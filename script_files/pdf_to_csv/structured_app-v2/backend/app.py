# backend/app.py
from flask import Flask, request, jsonify
import os
import pandas as pd
from extractor.extractor import extract_data
from services.logger import log_feedback
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from extractor.ocr_table import ocr_extract

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return 'PDF Extractor API Running'

from flask import jsonify
from extractor import extract_data

@app.route('/upload', methods=['POST'])
def upload():
    try:
        pdf = request.files['pdf']
        mode = request.form['mode']
        dpi = int(request.form['dpi'])

        save_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
        pdf.save(save_path)

        print(f"[INFO] Received {pdf.filename} with mode={mode} and dpi={dpi}")

        # 🔧 Call extraction logic
        df = extract_data(save_path, mode)
        csv_path = save_path.replace(".pdf", ".csv")
        df.to_csv(csv_path, index=False)

        return jsonify({
            "status": "success",
            "filename": pdf.filename,
            "mode_used": mode,
            "dpi": dpi,
            "csv_path": csv_path,
            "row_count": len(df),
            "message": "Extraction and save successful"
        }), 200

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
    
if __name__ == '__main__':
    app.run(port=5000)