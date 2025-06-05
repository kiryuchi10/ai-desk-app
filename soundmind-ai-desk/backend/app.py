from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import whisper
import openai
import datetime

# Load environment variables from .env
load_dotenv()

# ========== DATABASE SETUP ==========
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("MYSQL_PORT")
DB_NAME = os.getenv("MYSQL_DB")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChatLog(Base):
    __tablename__ = "chat_logs"
    id = Column(Integer, primary_key=True, index=True)
    duration = Column(Integer)
    text = Column(Text)
    keywords = Column(Text)
    response = Column(Text)
    timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

def insert_record(text, keywords, response):
    db = SessionLocal()
    new_entry = ChatLog(
        duration=len(text.split()),  # crude word-based duration estimate
        text=text,
        keywords=keywords,
        response=response
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    db.close()
    return new_entry.id


# ========== TRANSCRIBE AUDIO ==========
def transcribe_audio(file):
    model = whisper.load_model("base")
    file.save("temp.wav")
    result = model.transcribe("temp.wav")
    return result["text"]


# ========== ANALYZE & RESPOND ==========
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create client properly


def analyze_text_and_generate(text):
    # Extract keywords
    keyword_prompt = f"Extract 3 important keywords from this text: {text}"

    keyword_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful keyword extractor."},
            {"role": "user", "content": keyword_prompt}
        ]
    )

    keywords = keyword_response.choices[0].message.content

    # Generate reply
    reply_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": text}
        ]
    )

    response = reply_response.choices[0].message.content

    return {
        "transcribed_text": text,
        "keywords": keywords,
        "response": response
    }


# ========== FLASK APP ==========
app = Flask(__name__)
CORS(app)

@app.route("/api/voice", methods=["POST"])
def handle_voice():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    text = transcribe_audio(file)
    ai_result = analyze_text_and_generate(text)
    insert_record(text, ai_result['keywords'], ai_result['response'])
    return jsonify(ai_result)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "Missing text"}), 400

    result = analyze_text_and_generate(text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
