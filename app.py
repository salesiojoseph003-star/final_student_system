from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key="secret"

def db():
    conn=sqlite3.connect("db.db")
    conn.row_factory=sqlite3.Row
    return conn

@app.route("/", methods=["GET","POST"])
def index():
    if "user" not in session:
        return redirect("/login")
    conn=db()
    students=conn.execute("SELECT * FROM students").fetchall()
    marks=[s["marks"] for s in students]
    names=[s["name"] for s in students]
    conn.close()
    return render_template("dashboard.html",students=students,marks=marks,names=names)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]
        conn=db()
        user=conn.execute("SELECT * FROM users WHERE username=?",(u,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password"],p):
            session["user"]=u
            return redirect("/")
    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        u=request.form["username"]
        p=generate_password_hash(request.form["password"])
        conn=db()
        conn.execute("INSERT INTO users(username,password) VALUES (?,?)",(u,p))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/add",methods=["POST"])
def add():
    conn=db()
    conn.execute("INSERT INTO students(name,marks) VALUES (?,?)",
                 (request.form["name"],request.form["marks"]))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

app.run(debug=True)
