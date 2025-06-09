# Backend Setup (FastAPI)

## 1. Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Start API server
```bash
uvicorn app:app --reload
```

## 3. API Endpoints
| Method | Endpoint        | Description                |
|--------|------------------|----------------------------|
| POST   | `/upload`       | Upload PDF + extract table |
| GET    | `/status`       | Health check               |

## 4. Directory Structure
```
ai-pdf-extractor/
├── backend/
│   ├── app.py                # FastAPI entrypoint
│   ├── extractor.py          # Dispatch and table logic
│   ├── logger.py             # Logs user interaction
│   ├── hybrid_logic.py       # Combines OCR + table extraction
│   └── model_selector.py     # Optional: AI model selection
```

---

# MySQL Integration

## 1. MySQL Setup via CMD
```sql
CREATE DATABASE pdf_extraction;
USE pdf_extraction;

CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    resolution INT,
    detected_mode VARCHAR(50),
    user_confirmation VARCHAR(5),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 2. SQLAlchemy Database File: `database/db_setup.py`
```python
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = 'mysql+pymysql://user:password@localhost/pdf_extraction'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    resolution = Column(Integer)
    detected_mode = Column(String)
    user_confirmation = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
```

---

# CI/CD Setup (GitHub Actions + Netlify)

## 1. `.github/workflows/deploy.yml`
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run backend tests
        run: pytest

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run frontend build
        run: |
          cd frontend
          npm run build
      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v2.0
        with:
          publish-dir: ./frontend/build
          production-branch: main
          deploy-message: "Auto Deploy"
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

---


