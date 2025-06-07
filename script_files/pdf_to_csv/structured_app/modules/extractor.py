import pytesseract
from pdf2image import convert_from_path
import numpy as np
import cv2

def extract_by_mode(file_path, mode):
    page = convert_from_path(file_path, dpi=200)[0]
    image = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

    if mode == 'ocr':
        return pytesseract.image_to_string(image)

    elif mode == 'table':
        # Just simulate table detection
        return "Detected table and structured rows (simulate)."

    elif mode == 'hybrid':
        text = pytesseract.image_to_string(image)
        return f"[Hybrid] Table failed. OCR Fallback:\n{text}"
