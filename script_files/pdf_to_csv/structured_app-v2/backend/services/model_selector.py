# backend/model_selector.py
import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestClassifier
import joblib

DB_PATH = "database/feedback.db"
MODEL_PATH = "backend/model/extraction_mode_selector.pkl"

def train_model():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM feedback", conn)
    conn.close()

    df = df[df['user_confirmation'] == 'yes']
    if df.empty:
        return None

    X = df[['resolution']]
    y = df['detected_mode']
    model = RandomForestClassifier()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model

def predict_mode(resolution):
    model = joblib.load(MODEL_PATH)
    return model.predict([[resolution]])[0]
