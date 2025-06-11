def ocr_extract(file_path, dpi=300, poppler_path=r"C:\\poppler\\poppler-24.08.0\\Library\\bin"):
    from PIL import Image
    import pytesseract
    import cv2
    import numpy as np
    from pdf2image import convert_from_path
    import pandas as pd

    images = convert_from_path(file_path, dpi=dpi, poppler_path=poppler_path)
    if not images:
        print("[ERROR] No image extracted from PDF.")
        return pd.DataFrame()

    image = images[0]
    img_array = np.array(image)

    # Optional grayscale
    if len(img_array.shape) == 3:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    print("[DEBUG] Running OCR...")
    text = pytesseract.image_to_string(Image.fromarray(img_array))

    if not text.strip():
        print("[WARNING] OCR returned empty text.")
        return pd.DataFrame()

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    print(f"[DEBUG] Extracted {len(lines)} lines of text.")

    return pd.DataFrame(lines, columns=["extracted_text"])
