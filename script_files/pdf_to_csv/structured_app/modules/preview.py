import cv2
from pdf2image import convert_from_path
import numpy as np

def generate_preview(file_path, mode):
    page = convert_from_path(file_path, dpi=200)[0]
    image = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

    if mode == 'table':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        preview = cv2.bitwise_and(image, image, mask=lines)
        return preview
    return image
