import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import pandas as pd
import os

def extract_ocr(pdf_path, dpi=300, poppler_path=r"C:\poppler\poppler-24.08.0\Library\bin"):
    """
    Extracts text from a PDF using OCR (Tesseract) on full pages.
    Each line of text is returned as one entry in the result.
    """
    print("[INFO] Starting OCR-only extraction...")
    images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
    
    all_lines = []
    results_path = os.path.join("results", "ocr_pages")
    os.makedirs(results_path, exist_ok=True)

    for page_num, image in enumerate(images):
        print(f"[INFO] OCR processing page {page_num + 1}/{len(images)}")

        # Save image for debugging
        image_path = os.path.join(results_path, f"page_{page_num + 1}.png")
        image.save(image_path)

        # OCR
        config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=config)

        if text.strip():
            lines = text.strip().split('\n')
            for line in lines:
                clean = line.strip()
                if clean:
                    all_lines.append({
                        "page": page_num + 1,
                        "text": clean
                    })

    if not all_lines:
        print("[WARNING] No OCR text extracted.")
        return pd.DataFrame()

    df = pd.DataFrame(all_lines)
    return df
