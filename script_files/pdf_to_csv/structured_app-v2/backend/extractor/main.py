# main.py
from extractor.extractor import extract_by_mode

# Prompt user for input
pdf_path = input("Enter the full path to your PDF file: ").strip()

# Optional: allow user to choose extraction mode
print("Choose extraction mode: 'tabula', 'ocr', 'cv', or 'hybrid'")
mode = input("Mode: ").strip().lower()

# Optional: custom DPI input
try:
    dpi = int(input("Enter DPI (default 300): ").strip() or "300")
except ValueError:
    dpi = 300

# Run extraction
try:
    df = extract_by_mode(mode, pdf_path, dpi=dpi)
    print(df.head())
except Exception as e:
    print(f"[ERROR] Extraction failed: {e}")
