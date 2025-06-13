from flask import Blueprint, request, jsonify
import os
from extractor.ocr_table import extract_ocr
from extractor.cv_table import extract_cv
from extractor.hybrid_logic import hybrid_extract
from services.logger import log_feedback

UPLOAD_FOLDER = "backend/uploads"
RESULT_FOLDER = "backend/results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

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

    print(f"[INFO] Upload received: {pdf.filename} | mode={mode} | dpi={dpi}")

    try:
        # Dispatch to extraction mode
        if mode == 'ocr':
            df = extract_ocr(save_path)
        elif mode == 'table':
            df = extract_cv(save_path)
        elif mode == 'hybrid':
            df = hybrid_extract(save_path, dpi=dpi)
        else:
            return jsonify({"status": "error", "message": "Invalid extraction mode"}), 400

        if df is None or df.empty:
            return jsonify({
                "status": "error",
                "message": "No data extracted. Try increasing DPI or using another mode."
            }), 400

        csv_path = os.path.join(RESULT_FOLDER, pdf.filename.replace(".pdf", ".csv"))
        df.to_csv(csv_path, index=False)

        log_feedback(pdf.filename, mode, dpi, resolution=dpi, user_confirmation="pending")

        return jsonify({
            "status": "success",
            "message": "Extraction completed",
            "csv_path": csv_path,
            "row_count": len(df)
        })

    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
