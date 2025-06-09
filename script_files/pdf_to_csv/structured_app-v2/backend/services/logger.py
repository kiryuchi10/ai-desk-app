import pymysql
import os
from dotenv import load_dotenv

load_dotenv()  # Make sure .env file is in the project root

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB", "ai_feedback")
}

def log_feedback(filename, mode, dpi, resolution, user_confirmation):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255),
            mode VARCHAR(50),
            dpi INT,
            resolution INT,
            user_confirmation VARCHAR(10),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    sql = '''
        INSERT INTO feedback (filename, mode, dpi, resolution, user_confirmation)
        VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(sql, (filename, mode, dpi, resolution, user_confirmation))
    conn.commit()
    conn.close()
