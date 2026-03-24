from flask import Flask, render_template, request, jsonify, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS footprint (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car REAL,
        meat REAL,
        energy REAL,
        total REAL
    )
    """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")
from flask import redirect

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]

        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                       (username,password))
        user=cursor.fetchone()

        conn.close()

        if user:
            return redirect("/")
        else:
            return "Invalid login"

    return render_template("login.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    car = float(data["car"])
    meat = float(data["meat"])
    energy = float(data["energy"])

    total = (car*0.21)+(meat*2)+(energy*0.5)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO footprint (car, meat, energy, total) VALUES (?,?,?,?)",
                   (car, meat, energy, total))
    conn.commit()
    conn.close()

    return jsonify({"total": total})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000,debug=True)