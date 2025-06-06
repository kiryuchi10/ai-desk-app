import pdfplumber
import pytesseract
import pandas as pd
from tkinter import Tk, filedialog, simpledialog, messagebox
from PIL import Image
import os
import subprocess

# Set path to Tesseract OCR manually (if not in PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust if different

# Initialize GUI
root = Tk()
root.withdraw()  # Hide main window

# Ask user to choose a PDF file
pdf_path = filedialog.askopenfilename(
    title="Choose a PDF file",
    filetypes=[("PDF Files", "*.pdf")]
)

if not pdf_path or not os.path.exists(pdf_path):
    messagebox.showerror("Error", "No valid PDF file selected.")
    raise SystemExit("No file selected.")

# Ask user which mode to run
mode = simpledialog.askstring("Mode", "Choose mode:\n- ocr\n- table\n- hybrid", initialvalue="hybrid")
mode = mode.lower()

data_rows = []

# Begin parsing
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        table = page.extract_table()

        if mode in ["table", "hybrid"] and table:
            print(f"✅ Table found on page {i + 1}")
            for row in table:
                data_rows.append(row)
            continue

        if mode in ["ocr", "hybrid"]:
            print(f"🔍 OCR fallback for page {i + 1}")
            # Save page as image
            img_path = f"temp_page_{i + 1}.png"
            page.to_image(resolution=300).original.save(img_path)

            # OCR extract
            text = pytesseract.image_to_string(Image.open(img_path), config="--psm 6")
            os.remove(img_path)

            # Line split and tokenization
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            for line in lines:
                data_rows.append(line.split())

# Check and save result
if not data_rows:
    messagebox.showwarning("No Data", "No data extracted from the PDF.")
    raise SystemExit("No extractable content.")

# Heuristic: use first row as header if shape fits
columns = data_rows[0] if all(len(row) == len(data_rows[0]) for row in data_rows) else [f"Col{i}" for i in range(len(max(data_rows, key=len)))]
df = pd.DataFrame(data_rows[1:], columns=columns)

# Output file
output_csv = os.path.splitext(pdf_path)[0] + "_parsed.csv"
df.to_csv(output_csv, index=False)

# Notify and open
messagebox.showinfo("Success", f"Data saved to:\n{output_csv}")
subprocess.run(["explorer", output_csv])
