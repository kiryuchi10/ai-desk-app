# extractor.py
# Main dispatcher for different extraction modes + preview image support

import os
import pandas as pd

from PIL import ImageTk, Image
import tkinter as tk
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
from pdf2image import convert_from_path
import os
from .ocr_table import ocr_extract
from .cv_table import cv_extract
from .hybrid_logic import hybrid_extract
from .preview import generate_preview

def extract_data(file_path, mode):
    """
    Routes the PDF file to the correct extraction function based on the mode.
    Calls generate_preview() before starting extraction.

    Args:
        file_path (str): Path to the PDF file.
        mode (str): One of 'ocr', 'table', 'hybrid'.

    Returns:
        pd.DataFrame | None: Extracted data or None if cancelled
    """

    # ✅ Preview and confirm
    proceed = generate_preview(file_path)
    if not proceed:
        print("[INFO] Operation cancelled by user.")
        return None

    # ✅ Run extraction logic
    if mode == "ocr":
        print("[INFO] Running OCR-only extraction...")
        return ocr_extract(file_path)

    elif mode == "table":
        print("[INFO] Running table-only (OpenCV) extraction...")
        return cv_extract(file_path)

    elif mode == "hybrid":
        print("[INFO] Running hybrid extraction (table structure + OCR)...")
        return hybrid_extract(file_path)

    else:
        raise ValueError("Invalid mode: must be one of 'ocr', 'table', 'hybrid'")
