import tabula
import pandas as pd
import matplotlib.pyplot as plt
import os
from services.database_handler import save_dataframe_to_mysql, log_table_feedback

CLEANED_FOLDER = "backend/results/cleaned"
UNCLEANED_FOLDER = "backend/results/uncleaned"
os.makedirs(CLEANED_FOLDER, exist_ok=True)
os.makedirs(UNCLEANED_FOLDER, exist_ok=True)

def save_tables(tables, filename, mode, dpi):
    for idx, table in enumerate(tables):
        raw_path = os.path.join(UNCLEANED_FOLDER, f"{filename}_table{idx}_uncleaned.csv")
        clean_path = os.path.join(CLEANED_FOLDER, f"{filename}_table{idx}_cleaned.csv")

        table.to_csv(raw_path, index=False)
        save_dataframe_to_mysql(table, filename, mode, dpi, idx, is_cleaned=False)

        # Clean the table
        cleaned = table.dropna(axis=0, how='all').dropna(axis=1, how='all')
        cleaned.columns = [col if "Unnamed" not in col else f"col_{i}" for i, col in enumerate(cleaned.columns)]
        cleaned.to_csv(clean_path, index=False)
        save_dataframe_to_mysql(cleaned, filename, mode, dpi, idx, is_cleaned=True)

        # Log feedback for audit
        log_table_feedback(filename, idx, len(table), len(cleaned), table.shape[1], cleaned.shape[1], mode, dpi)

        print(f"[INFO] Table {idx}: saved cleaned and uncleaned versions.")

def extract_tabula(file_path, filename="unknown", mode="tabular", dpi=300):
    try:
        tables = tabula.read_pdf(file_path, pages='all', multiple_tables=True)

        if not tables:
            print("[ERROR] No tables found in PDF.")
            return pd.DataFrame()

        print(f"[INFO] {len(tables)} tables detected using Tabula.")
        for i, table in enumerate(tables):
            print(f"\n[Table {i+1}] Shape: {table.shape}")
            print(table.head(5))

        # Visualize table lengths
        try:
            table_lengths = [len(t) for t in tables]
            plt.figure(figsize=(10, 4))
            plt.bar([f"Table {i+1}" for i in range(len(tables))], table_lengths)
            plt.xlabel("Table Index")
            plt.ylabel("Row Count")
            plt.title("Number of Rows Detected per Table")
            plt.tight_layout()
            chart_path = os.path.join("backend/results", "table_chart.png")
            plt.savefig(chart_path)
            print(f"[INFO] Chart saved: {chart_path}")
        except Exception as e:
            print(f"[WARNING] Failed to plot table sizes: {e}")

        save_tables(tables, filename, mode, dpi)
        return max(tables, key=lambda x: len(x))

    except Exception as e:
        print(f"[ERROR] Tabular extraction failed: {e}")
        return pd.DataFrame()