# backend/routes/upload.py

from flask import Blueprint, request, jsonify
import os
from backend.extractor.ocr_table import ocr_extract
from backend.extractor.cv_table import cv_extract
from backend.extractor.hybrid_logic import hybrid_extract
from backend.services.logger import log_feedback

UPLOAD_FOLDER = "backend/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    pdf = request.files['pdf']
    mode = request.form.get('mode', 'ocr')
    dpi = int(request.form.get('dpi', 200))

    save_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
    pdf.save(save_path)

    try:
        # Route to the correct extractor
        if mode == 'ocr':
            data = ocr_extract(save_path)
        elif mode == 'table':
            data = cv_extract(save_path)
        elif mode == 'hybrid':
            data = hybrid_extract(save_path)
        else:
            return jsonify({"status": "error", "message": "Invalid mode"}), 400

        # Optionally log metadata
        log_feedback(resolution=dpi, detected_mode=mode, user_confirmation="pending")

        return jsonify({"status": "success", "data": data})

    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")
        return jsonify({"status": "error", "message": "Extraction failed"}), 500
