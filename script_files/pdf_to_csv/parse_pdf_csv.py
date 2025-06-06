import pdfplumber
import pandas as pd
import os

# Update this with your actual PDF file
pdf_path = r"C:\Users\user\Downloads\python_parse_data_pdf_csv\Share-20250606T214048Z-1-001\Share\example.pdf"
output_csv = "parsed_output.csv"

if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF not found: {pdf_path}")

data_rows = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            for row in table:
                data_rows.append(row)

# Convert to DataFrame
df = pd.DataFrame(data_rows[1:], columns=data_rows[0])
df.to_csv(output_csv, index=False)

print(f"Saved parsed data to {output_csv}")
