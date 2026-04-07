from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import io
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.secret_key="secret"

def db():
    conn=sqlite3.connect("db.db")
    conn.row_factory=sqlite3.Row
    return conn

def predict_performance(current_marks):
    """Simple AI prediction based on current marks"""
    if len(current_marks) < 2:
        return "Insufficient data for prediction"

    # Simple linear regression for trend
    X = np.array(range(len(current_marks))).reshape(-1, 1)
    y = np.array(current_marks)

    model = LinearRegression()
    model.fit(X, y)

    # Predict next performance
    next_x = np.array([[len(current_marks)]])
    predicted = model.predict(next_x)[0]

    # Calculate trend
    slope = model.coef_[0]
    if slope > 2:
        trend = "Strongly Improving"
    elif slope > 0:
        trend = "Improving"
    elif slope > -2:
        trend = "Stable"
    else:
        trend = "Declining"

    return {
        'predicted_marks': round(predicted, 1),
        'trend': trend,
        'confidence': min(95, 70 + abs(slope) * 10)  # Simple confidence calculation
    }

def generate_pdf_report(student_name, marks, prediction):
    """Generate PDF report for a student"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph(f"Student Performance Report - {student_name}", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Current Performance
    current_perf = Paragraph(f"Current Marks: {marks}", styles['Heading2'])
    story.append(current_perf)
    story.append(Spacer(1, 12))

    # Prediction
    if isinstance(prediction, dict):
        pred_text = f"""
        Expected Performance: {prediction['predicted_marks']}<br/>
        Trend: {prediction['trend']}<br/>
        Confidence: {prediction['confidence']}%
        """
    else:
        pred_text = f"Prediction: {prediction}"

    prediction_para = Paragraph(pred_text, styles['Normal'])
    story.append(prediction_para)

    doc.build(story)
    buffer.seek(0)
    return buffer

@app.route("/", methods=["GET","POST"])
def index():
    if "user" not in session:
        return redirect("/login")
    conn=db()
    students=conn.execute("SELECT * FROM students").fetchall()
    marks=[s["marks"] for s in students]
    names=[s["name"] for s in students]

    # Generate predictions for each student
    predictions = {}
    for student in students:
        # For demo, using current marks as historical data
        # In real app, you'd have multiple marks per student
        student_marks = [student["marks"]]  # Simplified
        predictions[student["id"]] = predict_performance(student_marks)

    conn.close()
    return render_template("dashboard.html",students=students,marks=marks,names=names,predictions=predictions)

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

@app.route("/download/<int:student_id>")
def download_report(student_id):
    if "user" not in session:
        return redirect("/login")

    conn = db()
    student = conn.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
    conn.close()

    if not student:
        return "Student not found", 404

    # Get prediction for this student
    student_marks = [student["marks"]]
    prediction = predict_performance(student_marks)

    # Generate PDF
    pdf_buffer = generate_pdf_report(student["name"], student["marks"], prediction)

    return send_file(pdf_buffer, as_attachment=True, download_name=f"{student['name']}_report.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
