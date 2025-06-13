# cv_table.py
import cv2
import numpy as np
from pdf2image import convert_from_path
import pandas as pd
import os
from PIL import Image

def extract_cv(file_path, dpi=300, poppler_path=r"C:\\poppler\\poppler-24.08.0\\Library\\bin"):
    images = convert_from_path(file_path, dpi=dpi, poppler_path=poppler_path)
    image = images[0]  # Only first page

    # Convert PIL to OpenCV
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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

    boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 40 and h > 20:
            boxes.append((x, y, x + w, y + h))

    boxes = sorted(boxes, key=lambda b: (b[1], b[0]))  # sort top to bottom, then left to right

    df = pd.DataFrame(boxes, columns=["x1", "y1", "x2", "y2"])
    return df