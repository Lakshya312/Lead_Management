import os
import pandas as pd

# Resolve the project root and data directory dynamically
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

def convert_excel_to_sanitized_csv(excel_filename):
    """
    Reads multi-sheet enterprise excel workbooks, sanitizes column definitions
    to standard lowercase format, and exports individual standalone CSV files.
    """
    excel_file_path = os.path.join(DATA_DIR, excel_filename)

    if not os.path.exists(excel_file_path):
        print(f"[Error] Target source file not located at: {excel_file_path}")
        return

    print(f"[Initialization] Processing master workbook: {excel_file_path}")
    excel_file = pd.ExcelFile(excel_file_path)

    for sheet_name in excel_file.sheet_names:
        print(f"-> Extracting structural layers from worksheet: {sheet_name}")
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        
        # Enforce strict system standards by down-casing column header arrays
        df.columns = [str(col).strip().lower() for col in df.columns]
        
        # Export CSV files into the data/ directory
        output_csv_path = os.path.join(DATA_DIR, f"{sheet_name.strip()}.csv")
        df.to_csv(output_csv_path, index=False)
        print(f"   [Success] Target system logs compiled into: {output_csv_path}")

    print("[Pipeline Complete] All operational master tables converted successfully.")

if __name__ == "__main__":
    # Point directly to your master data excel repository sheet name
    target_excel = "Product_Lead_Data_Demo.xlsx" 
    convert_excel_to_sanitized_csv(target_excel)