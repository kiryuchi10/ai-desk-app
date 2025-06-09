# Trains an AI model from feedback logs and predicts best extraction mode

import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestClassifier
import joblib  # For saving/loading model

DB_PATH = "database/feedback.db"
MODEL_PATH = "model/extraction_mode_selector.pkl"

def train_model():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM feedback", conn)
    conn.close()

    df = df[df['user_confirmation'] == 'yes']
    if df.empty:
        return None

    X = df[['resolution']]  # Add font, width/height in future
    y = df['detected_mode']
    model = RandomForestClassifier()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model

def predict_mode(resolution):
    model = joblib.load(MODEL_PATH)
    return model.predict([[resolution]])[0]
