from flask import Flask, request, redirect, session, render_template, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def homepage():
    loggedIn = 'username' in session
    username = session.get('username', '')
    isAdmin = session.get('isAdmin', False)
    return render_template("home.html", loggedIn=loggedIn, username=username, isAdmin=isAdmin)


@app.route('/history')
def history():
    loggedIn = 'username' in session
    username = session.get('username', '')
    isAdmin = session.get('isAdmin', False)
    return render_template("history.html", loggedIn=loggedIn, username=username, isAdmin=isAdmin)


@app.route('/all_teams')
def all_teams():
    loggedIn = 'username' in session
    username = session.get('username', '')
    isAdmin = session.get('isAdmin', False)
    return render_template("all_teams.html", loggedIn=loggedIn, username=username, isAdmin=isAdmin)


@app.route('/tipsandtricks')
def tipsandtricks():
    loggedIn = 'username' in session
    username = session.get('username', '')
    isAdmin = session.get('isAdmin', False)
    return render_template("tipsandtricks.html", loggedIn=loggedIn, username=username, isAdmin=isAdmin)


# Returns statistics data from the goalie database in SQL to the goaltender page
@app.route('/goalie/<int:id>')
def goaltender(id):
    loggedIn = 'username' in session
    username = session.get('username', '')
    isAdmin = session.get('isAdmin', False)
    conn = sqlite3.connect("goalies.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Statistics JOIN Goaltender ON Statistics.Goaltender_ID = Goaltender.ID WHERE ID=?;", (id,))
    goaltender = cur.fetchone()
    conn.close()
    return render_template('goaltender.html', goaltender=goaltender, loggedIn=loggedIn, username=username, isAdmin=isAdmin)


# Feedback page
@app.route('/feedback')
def feedback():
    loggedIn = 'username' in session
    username = session.get('username', '')
    isAdmin = session.get('isAdmin', False)
    if loggedIn:
        return render_template("feedback.html", loggedIn=loggedIn, username=username, isAdmin=isAdmin)
    else:
        flash('You need to log in to access this page.')
        return redirect('/login')


# Finished feedback page
@app.route('/submitedfeedback')
def submitedfeedback():
    loggedIn = 'username' in session
    username = session.get('username', '')
    isAdmin = session.get('isAdmin', False)
    if loggedIn:
        return render_template("submitedfeedback.html", loggedIn=loggedIn, username=username, isAdmin=isAdmin)
    else:
        flash('You need to log in to submit feedback.')
        return redirect('/login')


# Submits feedback into goalie database and directs user to a 'return to home page'
@app.route('/submitedfeedback', methods=['POST'])
def submit_feedback():
    if 'username' in session:
        username = session['username']
        message = request.form['message']
        topic = request.form['topic']

        conn = sqlite3.connect('goalies.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO Feedback (username, message, topic) VALUES (?,?,?)', (username, message, topic))
        conn.commit()
        conn.close()
        return redirect('/submitedfeedback')
    else:
        flash('You need to log in to submit feedback.')
        return redirect('/login')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


# login page
@app.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('goalies.db')
    user = conn.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()

    if user:
        session['username'] = username
        session['isAdmin'] = (username == 'admin')
        flash('Login successful!', 'success')
        return redirect('/')
    else:
        flash('An error occured, try again')

    return render_template('login.html')


# logging out
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('isAdmin', None)
    flash('You have been logged out.', 'success')
    return redirect('/')


# Sign up
@app.route('/signup', methods=['POST'])
def user_signup():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('goalies.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cur.fetchone()

    if user:
        flash('Username already exists. Please choose a different username.')
    else:
        cur.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        flash('Account created successfully! You can now log in.')
        return render_template("login.html")

    return render_template('signup.html')


# User stats table
@app.route('/createstats', methods=['GET', 'POST'])
def createstats():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            # Extract form data
            username = session['username']
            games_played = request.form['gamesPlayed']
            shutouts = request.form['shutouts']
            goalsagainstaverage = request.form['goalsagainstaverage']
            savepercentage = request.form['savepercentage']

            # SQL query
            sql = '''INSERT INTO Userstats (username, games_played, shutouts, goalsagainstaverage, savepercentage)
                     VALUES (?, ?, ?, ?, ?)'''

            # Database interaction
            conn = sqlite3.connect('goalies.db')
            cursor = conn.cursor()
            cursor.execute(sql, (username, games_played, shutouts, goalsagainstaverage, savepercentage))
            conn.commit()
            conn.close()

            flash('Stats created successfully!', 'success')

            return render_template('createstats.html', loggedIn=True)
        else:
            return render_template('createstats.html', loggedIn=True)
    else:
        flash('You need to log in to create stats.')
        return redirect('/login')


# Display for user stats
@app.route('/userstats')
def userstats():
    conn = sqlite3.connect('goalies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Userstats')
    Ustats = cursor.fetchall()
    conn.close()

    loggedIn = 'username' in session
    username = session.get('username', '')
    isAdmin = session.get('isAdmin', False)
    return render_template("userstats.html", loggedIn=loggedIn, Userstats=Ustats, username=username, isAdmin=isAdmin)


# Hidden admin page for feedback display
@app.route('/admin')
def admin():
    if 'username' in session and session['username'] == 'admin':
        conn = sqlite3.connect("goalies.db")
        cur = conn.cursor()
        cur.execute("SELECT username, message, topic FROM Feedback")
        feedback = cur.fetchall()
        conn.close()
        return render_template("admin.html", feedback=feedback, loggedIn=True, username=session['username'], isAdmin=True)
    else:
        flash('You need to log in as an admin to access this page.')
        return redirect('/login')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
