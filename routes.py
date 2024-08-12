from flask import Flask, request, redirect, session, render_template, flash, abort

import sqlite3

loggedIn = False
username = ''

admin = False

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def homepage():
    global loggedIn, username  # Define global variables
    if loggedIn:
        return render_template("home.html", loggedIn=loggedIn, username=username)
    else:
        return render_template("home.html", loggedIn=loggedIn)


@app.route('/history')
def history():
    return render_template("history.html")


@app.route('/all_teams')
def all_teams():
    return render_template("all_teams.html")


@app.route('/tipsandtricks')
def tipsandtricks():
    return render_template("tipsandtricks.html")


# Returns statistics data from the goalie database in SQL to the goaltender page
@app.route('/goalie/<int:id>')
def goaltender(id):
    conn = sqlite3.connect("goalies.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Statistics JOIN Goaltender ON Statistics.Goaltender_ID = Goaltender.ID WHERE ID=?;",(id,))
    goaltender = cur.fetchone()
    return render_template('goaltender.html', goaltender=goaltender)

# Feedback function...

# Feedback page
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


# Finished feedback page
@app.route('/submitedfeedback')
def submitedfeedback():
    return render_template('submitedfeedback.html')


# Submits feedback into goalie database and directs user to a 'return to home page'
@app.route('/submitedfeedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    message = request.form['message']
    topic = request.form['topic']
    conn = sqlite3.connect('goalies.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO Feedback (name, message, topic) VALUES (?,?,?)', (name, message, topic))
    conn.commit()
    conn.close()
    return redirect('/submitedfeedback')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


# login page
@app.route('/login', methods=['POST'])
def user_login():
    global loggedIn, username, admin  # Define global variables
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('goalies.db')
    user = conn.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()

    if user:
        loggedIn = True
        session['username'] = username
        flash('Login successful!', 'success')
        flash(f'Welcome back {username}')
        return redirect('/')
    else:
        flash('Invalid username or password', 'Try again')

    return render_template('login.html')


    # if username == 'admin' and password == 'qwerty':
    #     flash('Login successful!', 'success')
    #     loggedIn = True
    #     session['role'] = 'admin'
    #     flash(f'Welcome back {username}')
    #     return redirect('/')
    # elif user:
    #     flash('Login successful!', 'success')
    #     session['username'] = username
    #     flash(f'Welcome back {username}')
    #     loggedIn = True

    # if user:
    #     flash('Login successful!', 'success')
    #     session['username'] = username
    #     flash(f'Welcome back {username}')
    #     loggedIn = True
    # if username == "admin" and password == 'qwerty':
    #         session['loggedIn'] = True
    #         session['role'] = 'admin'
    #     return redirect('/')
    # else:
    #     flash('Invalid username or password', 'Try again')

    #     return render_template("login.html")  


# logging out  
@app.route('/logout', methods=['POST'])    
def logout():
    global loggedIn
    session.pop('username', None)
    session.pop('admin', None)
    loggedIn = False
    return render_template('home.html')


# Sign up
@app.route('/signup', methods=['POST'])
def user_signup():
    global loggedIn, username  # Define global variables
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
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
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


        return render_template('createstats.html')
    
    # Handle GET request
    return render_template('createstats.html')

# Display for user stats
@app.route('/userstats')
def userstats():
    conn = sqlite3.connect('goalies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Userstats')
    Ustats = cursor.fetchall()
    conn.close()
    return render_template('userstats.html', Userstats=Ustats)


# Hidden admin page for feedback display
@app.route('/admin')
def admin():
    global admin
    conn = sqlite3.connect("goalies.db")
    cur = conn.cursor()
    cur.execute("SELECT name, message, topic FROM Feedback")
    feedback = cur.fetchall()
    conn.close()
    return render_template("admin.html", feedback=feedback)

      # Define global variables
    # if not session.get('loggedIn') or session.get('username') != 'admin':
    #     return render_template('home.html')
    # return render_template('admin.html')

    # if 'username' in session and admin is True: 
        # conn = sqlite3.connect("goalies.db")
        # cur = conn.cursor()
        # cur.execute("SELECT name, message, topic FROM Feedback")
        # feedback = cur.fetchall()
        # conn.close()
        # return render_template("admin.html", feedback=feedback)
    # else:
    #     return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
