# MySQL Database Setup

```bash
# Start MySQL shell
mysql -u root -p

# Create database
CREATE DATABASE feedback_db;

# Use the database
USE feedback_db;

# Create feedback table
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    mode VARCHAR(50),
    feedback TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

# SQLAlchemy Example in Python

```python
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:password@localhost/feedback_db")
```