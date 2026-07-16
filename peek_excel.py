import pandas as pd
import sys

file_path = "../Liste des tableaux des Cadres logiques 19082024 Ok.xlsx"
try:
    xl = pd.ExcelFile(file_path)
    print("Sheets:", xl.sheet_names)
    for sheet in xl.sheet_names[:5]: # Peek at first 5 sheets
        df = pd.read_excel(file_path, sheet_name=sheet, nrows=5)
        print(f"\n--- Sheet: {sheet} ---")
        print(df.to_string())
except Exception as e:
    print(f"Error: {e}")
