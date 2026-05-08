from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "database/logs.db"

# Create database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

# Insert logs into database
def load_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM logs")

    with open("logs.txt", "r") as file:
        for line in file:
            parts = line.strip().split(" ", 1)

            if len(parts) == 2:
                level, message = parts
                cursor.execute(
                    "INSERT INTO logs (level, message) VALUES (?, ?)",
                    (level, message)
                )

    conn.commit()
    conn.close()

# Dashboard route
@app.route("/")
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM logs")
    logs = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM logs WHERE level='WARNING'")
    warnings = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE level='ERROR'")
    errors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE level='INFO'")
    infos = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        logs=logs,
        warnings=warnings,
        errors=errors,
        infos=infos
    )

if __name__ == "__main__":
    os.makedirs("database", exist_ok=True)

    init_db()
    load_logs()

    app.run(debug=True)