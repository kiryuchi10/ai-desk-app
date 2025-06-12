import pandas as pd
import numpy as np
import cv2
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os

def hybrid_extract(file_path, dpi=300, poppler_path=r"C:\\poppler\\poppler-24.08.0\\Library\\bin"):
    """
    Hybrid extraction: combines OpenCV table cell detection + OCR.
    Skips pages without valid cells. Saves debug images for review.
    """
    print("[INFO] Converting PDF to image pages...")
    images = convert_from_path(file_path, dpi=dpi, poppler_path=poppler_path)

    all_rows = []
    results_path = os.path.join("results", "debug_pages")
    os.makedirs(results_path, exist_ok=True)

    for page_num, image in enumerate(images):
        print(f"[INFO] Processing page {page_num + 1}/{len(images)}")

        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Line detection
        kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
        horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_h)
        vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_v)
        table_mask = cv2.add(horizontal, vertical)

        contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(f"[INFO] Page {page_num+1}: {len(contours)} possible cells")

        if not contours:
            print(f"[SKIP] Page {page_num+1} skipped (no tables found)")
            continue

        page_debug_boxes = []
        for idx, cnt in enumerate(contours):
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 40 and h > 20:
                roi = img_cv[y:y+h, x:x+w]
                roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                roi_thresh = cv2.adaptiveThreshold(roi_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                   cv2.THRESH_BINARY, 15, 8)
                roi_pil = Image.fromarray(roi_thresh)

                config = r'--oem 3 --psm 6'
                text = pytesseract.image_to_string(roi_pil, config=config)

                if text.strip():
                    all_rows.append({
                        "page": page_num + 1,
                        "x1": x, "y1": y, "x2": x + w, "y2": y + h,
                        "text": text.strip()
                    })
                    print(f"[DEBUG] Page {page_num+1} Cell {idx}: size=({w}x{h}) Text: '{text.strip()[:50]}'")
                    page_debug_boxes.append((x, y, w, h))

        # Draw all boxes found on full page for debug
        if page_debug_boxes:
            for (x, y, w, h) in page_debug_boxes:
                cv2.rectangle(img_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)

            debug_img_path = os.path.join(results_path, f"page{page_num+1}_full.png")
            cv2.imwrite(debug_img_path, img_cv)
            print(f"[INFO] Saved debug image: {debug_img_path} with {len(page_debug_boxes)} boxes")

    if not all_rows:
        print("[WARNING] No OCR text extracted from any page.")
        return pd.DataFrame()

    print(f"[INFO] Total extracted entries: {len(all_rows)}")
    return pd.DataFrame(all_rows)
