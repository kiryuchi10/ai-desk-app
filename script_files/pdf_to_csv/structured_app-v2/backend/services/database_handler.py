import mysql.connector
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="pdf_extraction"
    )

def save_dataframe_to_mysql(df, filename, mode, dpi, table_index, is_cleaned):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        table_name = "extracted_data_cleaned" if is_cleaned else "extracted_data_raw"
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255),
                table_index INT,
                mode VARCHAR(20),
                dpi INT,
                data LONGTEXT,
                is_cleaned BOOLEAN,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        data_str = df.to_csv(index=False)
        cursor.execute(f"""
            INSERT INTO {table_name} (filename, table_index, mode, dpi, data, is_cleaned)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (filename, table_index, mode, dpi, data_str, is_cleaned))

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"[ERROR] Failed to save to MySQL: {e}")


def log_table_feedback(filename, table_index, raw_rows, clean_rows, raw_cols, clean_cols, mode, dpi):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS table_extraction_feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255),
                table_index INT,
                original_rows INT,
                cleaned_rows INT,
                original_cols INT,
                cleaned_cols INT,
                mode VARCHAR(20),
                dpi INT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            INSERT INTO table_extraction_feedback
            (filename, table_index, original_rows, cleaned_rows, original_cols, cleaned_cols, mode, dpi)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (filename, table_index, raw_rows, clean_rows, raw_cols, clean_cols, mode, dpi))

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"[ERROR] Failed to log feedback: {e}")
