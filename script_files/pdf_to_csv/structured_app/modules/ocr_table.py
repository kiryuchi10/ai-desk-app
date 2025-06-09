# ocr_table.py
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
from PIL import Image

def ocr_extract(file_path):
    pages = convert_from_path(file_path, dpi=300, poppler_path=r"C:\poppler\poppler-24.08.0\Library\bin")
    text_data = []
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page, config="--psm 6")
        text_data.append({"page": i + 1, "text": text})

    df = pd.DataFrame(text_data)
    return df
