# extractor/extractor.py
from extractor.ocr_table import extract_ocr
from extractor.cv_table import extract_cv
from extractor.hybrid_logic import hybrid_extract
from extractor.tabular_extractor import extract_tabula

def extract_data(file_path, mode='hybrid', dpi=300):
    if mode == 'ocr':
        from extractor.ocr_table import extract_ocr
        return extract_ocr(file_path, dpi)
    elif mode == 'hybrid':
        from extractor.hybrid_logic import extract_hybrid
        return extract_hybrid(file_path, dpi)
    elif mode == 'cv':
        from extractor.cv_table import extract_cv
        return extract_cv(file_path, dpi)
    elif mode == 'tabular':
        from extractor.tabular_extractor import extract_tabular
        return extract_tabular(file_path)
    else:
        raise ValueError(f"Unknown extraction mode: {mode}")
