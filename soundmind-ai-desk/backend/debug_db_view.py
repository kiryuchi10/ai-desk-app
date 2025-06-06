# debug_db_view.py
from sqlalchemy.orm import Session
from app import SessionLocal, ChatLog

db: Session = SessionLocal()
for entry in db.query(ChatLog).all():
    print(f"[{entry.timestamp}] {entry.text} => {entry.response}")
db.close()
