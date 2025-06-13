# extractor/extractor.py

from extractor.ocr_table import extract_ocr
from extractor.cv_table import extract_cv
from extractor.hybrid_logic import hybrid_extract
from extractor.tabular_extractor import extract_tabula  #correct function name

def extract_data(file_path, mode='hybrid', dpi=300):
    if mode == 'ocr':
        return extract_ocr(file_path, dpi)
    elif mode == 'hybrid':
        return hybrid_extract(file_path, dpi)
    elif mode == 'cv':
        return extract_cv(file_path, dpi)
    elif mode == 'tabular':
        return extract_tabula(file_path)  #fixed usage
    else:
        raise ValueError(f"Unknown extraction mode: {mode}")
