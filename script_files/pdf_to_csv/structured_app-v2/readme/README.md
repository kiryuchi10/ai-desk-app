# Project Learning Notes

## Objective
Build a hybrid OCR + Table detection PDF extractor that previews and logs feedback using SQLite.

## Algorithms Tried
- OpenCV line detection
- Tesseract OCR
- TableNet (planned)
- CNN+RNN (planned)

## Challenges
- Poppler PATH issues on Windows
- Poor performance on rotated scans
- Feedback schema design

## Improvements
- Add ML model selector
- Learn from user feedback loop


## Setup
- Directory Structure
-- mkdir -p pdf-structure-ai-extractor/{01_requirements_analysis,02_architecture_design,03_ai_ocr_models,04_computer_vision,05_ml_optimization,06_theory_and_papers,backend,frontend,database,datasets/sample_pdfs,datasets/test_outputs} && cd pdf-structure-ai-extractor && touch README.md setup.md LICENSE .gitignore
 

 # PDF Structure AI Extractor

A complete AI-assisted tool that extracts structured tabular data from government PDF documents using a hybrid of OCR and OpenCV-based table detection, trained and optimized using deep learning.

## 🔍 Features
- OCR with multilingual support (Tesseract, CRNN)
- Table structure detection using OpenCV + ML heuristics
- Mode selection: OCR-only, Table-only, or Hybrid
- SQLite-based feedback logger for retraining

## 🧠 Technical Stack
- React + Flask
- Python (cv2, pytesseract, pdf2image, SQLAlchemy)
- TensorFlow, Scikit-Learn
- SQLite, MySQL (optional)

## 📚 Study References
| Process Area                | Book Title                                                | Focus                                  |
|----------------------------|-----------------------------------------------------------|----------------------------------------|
| Requirements & Design      | Software Engineering - Ian Sommerville                   | SDLC, Documentation                    |
| Architecture & Scaling     | Designing Data-Intensive Applications - M. Kleppmann     | Data Models, Flow, Resilience          |
| OCR/AI Design              | Deep Learning for Vision Systems - Mohamed Elgendy       | Model Structure, Deployment            |
| Computer Vision            | Programming CV with Python - Jan Erik Solem             | OpenCV, Contour Detection              |
| ML Optimization            | Hands-On ML with Scikit-Learn, Keras, TF                 | Hyperparam Tuning, Pipeline            |
| Theoretical ML & Papers    | The Elements of Statistical Learning                     | Statistical Foundations, Generalization|

## 🗃️ Directory Overview
- `01_requirements_analysis/`: Use cases, system requirements
- `03_ai_ocr_models/`: OCR pipeline, AI training notebook
- `backend/`: FastAPI routes & AI model API
- `frontend/`: React component structure
