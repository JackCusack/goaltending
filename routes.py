from flask import Flask, request, render_template, redirect, flash, session
import sqlite3
app = Flask(__name__)
app.secret_key ='your_secret_key'

@app.route('/')
def homepage():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return render_template("home.html", username=username)

@app.route('/history')
def history():
    return render_template("history.html")

@app.route('/all_teams')
def all_teams():
    return render_template("all_teams.html")

@app.route('/tipsandtricks')
def tipsandtricks():
    return render_template("tipsandtricks.html")

#Returns statistics data from the goalie database in SQL to the goaltender page
@app.route('/goalie/<int:id>')
def goaltender(id):
    conn = sqlite3.connect("goalies.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Statistics JOIN Goaltender ON Statistics.Goaltender_ID = Goaltender.ID WHERE ID=?;",(id,))
    goaltender = cur.fetchone()
    return render_template('goaltender.html', goaltender=goaltender)

#Feedback function...

#Feedback page
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

#Finished feedback page
@app.route('/submitedfeedback')
def submitedfeedback():
    return render_template('submitedfeedback.html')

#Submits feedback into goalie database and directs user to a 'return to home page'
@app.route('/submitedfeedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    message = request.form['message']
    topic = request.form['topic']
    conn  = sqlite3.connect('goalies.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO Feedback (name, message, topic) VALUES (?,?,?)', (name, message, topic))
    conn.commit()
    conn.close()
    return redirect('/submitedfeedback')

#Hidden admin page for feedback display
@app.route('/admin')
def admin():
    conn = sqlite3.connect("goalies.db")
    cur = conn.cursor()
    cur.execute("SELECT name, message, topic FROM Feedback")
    feedback = cur.fetchall()
    conn.close()
    return render_template("admin.html", feedback=feedback)

#Login and sign up  function...

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

#login 
@app.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('goalies.db')
    user = conn.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.commit()
    conn.close()

    if user:
        session['username'] = username
        flash('Login successful!', 'success')
        return render_template("home.html")
    else:
        flash('Invalid username or password', 'Try again')
        return render_template("login.html")
    
#Sign up
@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('goalies.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Users WHERE username = ?", (username,))
            user = cur.fetchone()
            if user:
                flash('Username already exists. Please choose a different username.')
            else:
                cur.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                flash('Account created successfully! You can now log in.')
                return render_template("login.html")

        return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)