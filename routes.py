from flask import Flask, request, render_template, redirect
import sqlite3
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("home.html")

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

if __name__ == "__main__":
    app.run(debug=True)