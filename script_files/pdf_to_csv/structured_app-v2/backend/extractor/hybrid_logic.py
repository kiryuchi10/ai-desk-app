import pandas as pd
import numpy as np
import cv2
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os

def hybrid_extract(file_path, dpi=300, poppler_path=r"C:\\poppler\\poppler-24.08.0\\Library\\bin"):
    """
    Combines table structure detection with OCR text extraction.
    Extracts cell bounding boxes with OpenCV, then OCRs each cell.

    Args:
        file_path (str): path to the PDF file
        dpi (int): image resolution for conversion

    Returns:
        pd.DataFrame: structured OCR results with coordinates
    """

    print("[INFO] Converting PDF to image...")
    images = convert_from_path(file_path, dpi=dpi, poppler_path=poppler_path)
    image = images[0]  # only first page for now

    # Convert to OpenCV format
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Detect lines
    kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_h)
    vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_v)
    table_mask = cv2.add(horizontal, vertical)

    # Find contours
    contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"[INFO] Found {len(contours)} potential table cells")

    rows = []
    results_path = os.path.join("results")
    os.makedirs(results_path, exist_ok=True)

    for idx, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 40 and h > 20:
            roi = img_cv[y:y+h, x:x+w]
            roi_pil = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))

            debug_path = os.path.join(results_path, f"debug_cell_{idx}.png")
            roi_pil.save(debug_path)

            custom_config = r'--oem 3 --psm 11'
            text = pytesseract.image_to_string(roi_pil, config=custom_config, lang='eng')

            if text.strip():
                rows.append({
                    "x1": x, "y1": y, "x2": x + w, "y2": y + h,
                    "text": text.strip()
                })
            else:
                print(f"[EMPTY] No text found in cell {idx} at ({x},{y},{w},{h})")

    if not rows:
        print("[WARNING] No table cells with text found.")
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    return df
