from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("layout.html")

@app.route('/history')
def history():
    return render_template("layout.html")

@app.route('/all_teams')
def all_teams():
    return "all_teams"

@app.route('/goalie/<int:id>')
def goaltender(id):
    conn = sqlite3.connect("goalies.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Statistics JOIN Goaltender ON Statistics.Goaltender_ID = Goaltender.ID WHERE ID=?;",(id,))
    # cur.execute("SELECT * FROM Goaltender WHERE Goaltender_ID=?",(id,))
    goaltender = cur.fetchone()
    return render_template('goaltender.html', goaltender=goaltender)


if __name__ == "__main__":
    app.run(debug=True)
 
#  WHERE Goaltender_ID=?",(id,))
    
