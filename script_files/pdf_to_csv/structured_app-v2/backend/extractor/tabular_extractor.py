# extractor/tabular_extractor.py
import tabula
import pandas as pd

def extract_tabula(pdf_path: str, pages='all'):
    print(f"[INFO] Extracting using Tabula on pages: {pages}")
    try:
        dfs = tabula.read_pdf(pdf_path, pages=pages, multiple_tables=True, lattice=False)
        results = pd.concat(dfs, ignore_index=True)
        print(f"[INFO] Extracted {len(results)} rows")
        return results
    except Exception as e:
        print(f"[ERROR] Tabula extraction failed: {e}")
        return pd.DataFrame()
