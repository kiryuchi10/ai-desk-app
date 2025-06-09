# hybrid_logic.py
from .ocr_table import ocr_extract
from .cv_table import cv_extract
import pandas as pd

def hybrid_extract(file_path):
    ocr_df = ocr_extract(file_path)
    cv_df = cv_extract(file_path)

    # Basic merge by page number
    merged_df = pd.merge(ocr_df, cv_df, how="outer", on="page")
    return merged_df
