# backend/services/logger.py

def log_feedback(filename, mode, dpi, resolution, user_confirmation):
    ...
    sql = '''
        INSERT INTO feedback (filename, mode, dpi, resolution, user_confirmation)
        VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(sql, (filename, mode, dpi, resolution, user_confirmation))
