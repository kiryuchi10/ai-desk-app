# extractor.py
# Main dispatcher for different extraction modes + optional visual preview

import pandas as pd
from .ocr_table import ocr_extract
from .cv_table import cv_extract
from .hybrid_logic import hybrid_extract

import cv2
import numpy as np
from pdf2image import convert_from_path

# ---------- Main Extraction Dispatcher ----------
def extract_data(file_path, mode):
    """
    Routes the PDF file to the correct extraction function based on the mode.

    Args:
        file_path (str): Path to the PDF file.
        mode (str): One of 'ocr', 'table', 'hybrid'.

    Returns:
        pd.DataFrame: Extracted data in structured table form.
    """
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


# ---------- Visual Preview Function ----------
import cv2
import numpy as np
import tkinter as tk
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
from pdf2image import convert_from_path
import os

def generate_preview(file_path):
    root = Tk()
    root.title("Preview")

    img = Image.open("preview_with_grid.png").resize((800, 1000))
    tk_img = ImageTk.PhotoImage(img)  # Must happen after root

    label = Label(root, image=tk_img)
    label.image = tk_img              # ✅ Prevent garbage collection
    label.pack()

    result = {"user_choice": False}

    def on_yes(): result["user_choice"] = True; root.destroy()
    def on_no(): root.destroy()

    Button(root, text="Yes", command=on_yes).pack(side="left")
    Button(root, text="No", command=on_no).pack(side="right")

    root.mainloop()
    return result["user_choice"]
