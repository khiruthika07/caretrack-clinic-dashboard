from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime, date, timedelta
from pathlib import Path
import math

app = Flask(__name__)
app.secret_key = "caretrack-local-demo"
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "caretrack.db"

DEMO_APPOINTMENTS = [
    ("CT-1001", "Aarav Kumar", "Dr. Meera Shah", "Cardiology", "09:00", "Completed", 10),
    ("CT-1002", "Diya Raman", "Dr. Arjun Rao", "General Medicine", "09:30", "Completed", 12),
    ("CT-1003", "Rahul Nair", "Dr. Meera Shah", "Cardiology", "10:00", "Waiting", 18),
    ("CT-1004", "Ananya Iyer", "Dr. Priya Menon", "Dermatology", "10:30", "Delayed", 27),
    ("CT-1005", "Vikram Das", "Dr. Arjun Rao", "General Medicine", "11:00", "Upcoming", 8),
    ("CT-1006", "Nisha Patel", "Dr. Priya Menon", "Dermatology", "11:30", "Upcoming", 6),
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT UNIQUE NOT NULL,
            patient TEXT NOT NULL,
            doctor TEXT NOT NULL,
            department TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT NOT NULL,
            wait_minutes INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    count = conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]
    if count == 0:
        now = datetime.now().isoformat(timespec="seconds")
        conn.executemany("""
            INSERT INTO appointments
            (token, patient, doctor, department, time, status, wait_minutes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [(*row, now) for row in DEMO_APPOINTMENTS])
    conn.commit()
    conn.close()

def dashboard_stats(conn):
    total = conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]
    completed = conn.execute("SELECT COUNT(*) FROM appointments WHERE status='Completed'").fetchone()[0]
    waiting = conn.execute("SELECT COUNT(*) FROM appointments WHERE status='Waiting'").fetchone()[0]
    delayed = conn.execute("SELECT COUNT(*) FROM appointments WHERE status='Delayed'").fetchone()[0]
    upcoming = conn.execute("SELECT COUNT(*) FROM appointments WHERE status='Upcoming'").fetchone()[0]
    avg_wait = conn.execute("SELECT COALESCE(AVG(wait_minutes),0) FROM appointments").fetchone()[0]
    return {
        "total": total, "completed": completed, "waiting": waiting,
        "delayed": delayed, "upcoming": upcoming,
        "avg_wait": round(avg_wait or 0)
    }

@app.route("/")
def dashboard():
    conn = get_db()
    stats = dashboard_stats(conn)
    appointments = conn.execute("SELECT * FROM appointments ORDER BY time").fetchall()
    doctors = [
        {"name": "Dr. Meera Shah", "specialty": "Cardiology", "patients": 8, "status": "In consultation", "color": "violet"},
        {"name": "Dr. Arjun Rao", "specialty": "General Medicine", "patients": 5, "status": "Available", "color": "blue"},
        {"name": "Dr. Priya Menon", "specialty": "Dermatology", "patients": 6, "status": "In consultation", "color": "rose"},
    ]
    conn.close()
    return render_template("dashboard.html", stats=stats, appointments=appointments, doctors=doctors, today=date.today().strftime("%A, %d %B %Y"))

@app.route("/appointments")
def appointments():
    conn = get_db()
    rows = conn.execute("SELECT * FROM appointments ORDER BY time").fetchall()
    conn.close()
    return render_template("appointments.html", appointments=rows)

@app.route("/appointments/add", methods=["POST"])
def add_appointment():
    patient = request.form.get("patient", "").strip()
    doctor = request.form.get("doctor", "").strip()
    department = request.form.get("department", "").strip()
    time = request.form.get("time", "").strip()
    if not all([patient, doctor, department, time]):
        flash("Please complete all appointment fields.", "error")
        return redirect(url_for("appointments"))

    conn = get_db()
    token_num = conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0] + 1001
    token = f"CT-{token_num}"
    conn.execute("""
        INSERT INTO appointments
        (token, patient, doctor, department, time, status, wait_minutes, created_at)
        VALUES (?, ?, ?, ?, ?, 'Upcoming', 0, ?)
    """, (token, patient, doctor, department, time, datetime.now().isoformat(timespec="seconds")))
    conn.commit()
    conn.close()
    flash(f"Appointment {token} created successfully.", "success")
    return redirect(url_for("appointments"))

@app.route("/appointments/<int:appointment_id>/status", methods=["POST"])
def update_status(appointment_id):
    status = request.form.get("status")
    allowed = {"Completed", "Waiting", "Delayed", "Upcoming"}
    if status not in allowed:
        return jsonify({"error": "Invalid status"}), 400
    conn = get_db()
    conn.execute("UPDATE appointments SET status=? WHERE id=?", (status, appointment_id))
    conn.commit()
    conn.close()
    return redirect(url_for("appointments"))

@app.route("/api/overview")
def overview():
    conn = get_db()
    stats = dashboard_stats(conn)
    conn.close()
    return jsonify(stats)

@app.route("/reset-demo", methods=["POST"])
def reset_demo():
    conn = get_db()
    conn.execute("DELETE FROM appointments")
    now = datetime.now().isoformat(timespec="seconds")
    conn.executemany("""
        INSERT INTO appointments
        (token, patient, doctor, department, time, status, wait_minutes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [(*row, now) for row in DEMO_APPOINTMENTS])
    conn.commit()
    conn.close()
    flash("Demo data restored.", "success")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
