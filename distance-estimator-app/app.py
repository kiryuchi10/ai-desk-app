# app.py
from flask import Flask, request, jsonify
from utils import estimate_distance
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/distance", methods=["POST"])
def calculate_distance():
    data = request.json
    result = estimate_distance(
        float(data['objectWidth']),
        float(data['fingerWidth']),
        float(data['armLength'])
    )
    return jsonify({"distance": result})
