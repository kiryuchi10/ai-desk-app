import sqlite3
import os

def log_feedback(file_path, mode, confirmation):
    db_path = os.path.join(os.path.dirname(__file__), "../extraction_feedback.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        resolution INTEGER,
        detected_mode TEXT,
        user_confirmation TEXT,
        font TEXT,
        feedback_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    INSERT INTO feedback (file_name, resolution, detected_mode, user_confirmation, font)
    VALUES (?, ?, ?, ?, ?)
    ''', (file_path, 200, mode, confirmation, "Unknown"))

    conn.commit()
    conn.close()
