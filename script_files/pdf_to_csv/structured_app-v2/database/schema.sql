CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    mode TEXT,
    dpi INTEGER,
    resolution INTEGER,
    user_confirmation TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
