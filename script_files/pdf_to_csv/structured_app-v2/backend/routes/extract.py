import os
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/preview/<filename>")
def preview_extracted_tables(filename):
    folder = os.path.join("backend/results/cleaned")
    matched = [f for f in os.listdir(folder) if filename in f and f.endswith(".csv")]

    result = {}
    for f in matched:
        df = pd.read_csv(os.path.join(folder, f))
        result[f] = df.to_dict(orient="records")

    return jsonify(result)
