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

# modules/preview_pyqt.py

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import os

def generate_preview(file_path):
    """
    Displays a preview image with Yes/No buttons using PyQt5.
    Returns True if user confirms, False otherwise.
    """
    class PreviewWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("PDF Preview Confirmation")
            self.setGeometry(100, 100, 850, 1050)
            self.result = False

            layout = QVBoxLayout()

            # Load the preview image
            preview_path = "preview_with_grid.png"
            if not os.path.exists(preview_path):
                print("[ERROR] Preview image not found.")
                sys.exit()

            pixmap = QPixmap(preview_path).scaled(800, 1000)
            self.label = QLabel()
            self.label.setPixmap(pixmap)

            layout.addWidget(self.label)

            # Buttons
            button_layout = QHBoxLayout()
            yes_btn = QPushButton("Yes")
            no_btn = QPushButton("No")
            yes_btn.clicked.connect(self.yes_clicked)
            no_btn.clicked.connect(self.no_clicked)
            button_layout.addWidget(yes_btn)
            button_layout.addWidget(no_btn)

            layout.addLayout(button_layout)
            self.setLayout(layout)

        def yes_clicked(self):
            self.result = True
            self.close()

        def no_clicked(self):
            self.result = False
            self.close()

    app = QApplication(sys.argv)
    preview_window = PreviewWindow()
    preview_window.show()
    app.exec_()

    return preview_window.result
