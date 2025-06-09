# cv_table.py
import cv2
import numpy as np
from pdf2image import convert_from_path
import pandas as pd

def cv_extract(file_path):
    images = convert_from_path(file_path, dpi=300, poppler_path=r"C:\poppler\poppler-24.08.0\Library\bin")
    results = []

    for idx, image in enumerate(images):
        img_path = f"page_{idx+1}.png"
        image.save(img_path, "PNG")

        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        adaptive = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                         cv2.THRESH_BINARY_INV, 15, 8)

        # Morphological transformation
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 2))
        dilated = cv2.dilate(adaptive, kernel, iterations=1)

        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rows = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 100 and h > 15:
                rows.append({"page": idx+1, "x": x, "y": y, "w": w, "h": h})

        results.extend(rows)

    return pd.DataFrame(results)
