# main.py
import os
from modules.extractor import extract_data, generate_preview
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

def process_pdf(file_path, mode):
    print(f"\n=== Processing: {file_path} ===")

    # Step 1: Show preview
    confirmed = generate_preview(file_path)
    if not confirmed:
        print("[INFO] Operation cancelled by user.")
        return

    # Step 2: Extract data
    try:
        extracted_data = extract_data(file_path, mode)
        if extracted_data is None or extracted_data.empty:
            print("[WARNING] No data extracted.")
            return

        # Step 3: Save results
        base_name = os.path.basename(file_path).replace(".pdf", "")
        output_path = os.path.join("results", "outputs", f"{base_name}_{mode}.csv")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        extracted_data.to_csv(output_path, index=False)
        print(f"[INFO] Saved to: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to process file: {e}")

def main():
    print("=== PDF Table/OCR Parser ===")

    mode_map = {"1": "ocr", "2": "table", "3": "hybrid"}
    choice = input("Select extraction mode:\n1. OCR only\n2. Table detection only\n3. Hybrid (table + OCR)\nEnter choice (1/2/3): ").strip()
    mode = mode_map.get(choice, "ocr")

    batch = input("Process (1) Single PDF or (2) All PDFs in a folder? ").strip()
    if batch == "2":
        Tk().withdraw()
        folder_path = askdirectory(title="Select a folder with PDF files")
        if not folder_path:
            print("[INFO] No folder selected.")
            return
        pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")]
        for pdf_path in pdf_files:
            process_pdf(pdf_path, mode)
    else:
        Tk().withdraw()
        pdf_path = askopenfilename(title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")])
        if pdf_path:
            process_pdf(pdf_path, mode)
        else:
            print("[INFO] No file selected.")

if __name__ == "__main__":
    main()
