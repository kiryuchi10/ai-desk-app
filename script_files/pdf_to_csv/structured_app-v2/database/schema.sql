-- schema.sql
CREATE TABLE feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  filename TEXT,
  mode TEXT,
  performance TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);