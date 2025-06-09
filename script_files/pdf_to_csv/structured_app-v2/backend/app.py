# backend/app.py
from flask import Flask, request
import os
app = Flask(__name__)

@app.route('/')
def home():
    return 'PDF Extractor API Running'


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    pdf = request.files['pdf']
    mode = request.form['mode']
    dpi = int(request.form['dpi'])

    save_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
    pdf.save(save_path)

    # Call your extract_data() here
    print(f"[INFO] Received {pdf.filename} with mode={mode} and dpi={dpi}")
    return {"status": "success", "message": "File processed"}

if __name__ == '__main__':
    app.run(port=5000)
