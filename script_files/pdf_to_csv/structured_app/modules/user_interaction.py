import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
import cv2

def ask_mode():
    root = tk.Tk()
    root.withdraw()
    mode = simpledialog.askstring("Mode Selection", "Enter extraction mode: table / ocr / hybrid")
    return mode.lower()

def confirm_preview(preview_img):
    plt.imshow(cv2.cvtColor(preview_img, cv2.COLOR_BGR2RGB))
    plt.title("Confirm preview: Close image to continue")
    plt.axis('off')
    plt.show()

    root = tk.Tk()
    root.withdraw()
    return messagebox.askyesno("Confirm", "Proceed with this detection?")
