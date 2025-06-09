# modules/logger.py
import sqlite3
import os

def log_result(file_path, mode, output_file, success=True, notes=""):
    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "feedback.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT,
            mode TEXT,
            output_file TEXT,
            success INTEGER,
            notes TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        INSERT INTO logs (file_path, mode, output_file, success, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (file_path, mode, output_file, int(success), notes))

    conn.commit()
    conn.close()
