# backend/extractor.py
def extract_data(file_path, mode):
    from extractor.hybrid_logic import hybrid_extract
    from extractor.cv_table import cv_extract
    from extractor.ocr_table import ocr_extract

    if mode == 'ocr':
        return ocr_extract(file_path)
    elif mode == 'table':
        return cv_extract(file_path)
    elif mode == 'hybrid':
        return hybrid_extract(file_path)
    else:
        return None
