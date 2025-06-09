# ocr_table.py
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
from PIL import Image
import numpy as np
import os

def ocr_extract(file_path, dpi=300, poppler_path=r"C:\\poppler\\poppler-24.08.0\\Library\\bin"):
    images = convert_from_path(file_path, dpi=dpi, poppler_path=poppler_path)
    image = images[0]  # First page only

    # Convert to grayscale if needed
    img_array = np.array(image)
    if len(img_array.shape) == 3:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    text = pytesseract.image_to_string(Image.fromarray(img_array))

    lines = text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    df = pd.DataFrame(lines, columns=["extracted_text"])
    return df