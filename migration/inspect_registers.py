import os
import pandas as pd

SOURCE_DIR = "migration/source_registers"

def inspect_file(path):
    try:
        xls = pd.ExcelFile(path)
        sheets = xls.sheet_names

        summary = {
            "file": os.path.basename(path),
            "sheets": len(sheets),
            "sheet_names": sheets
        }

        # inspect first sheet only for structure
        df = xls.parse(sheets[0])

        summary["columns"] = list(df.columns)
        summary["rows"] = len(df)

        return summary

    except Exception as e:
        return {
            "file": os.path.basename(path),
            "error": str(e)
        }

def run():
    results = []

    for f in os.listdir(SOURCE_DIR):
        if f.endswith(".xlsx"):
            path = os.path.join(SOURCE_DIR, f)
            results.append(inspect_file(path))

    for r in results:
        print("\n---")
        for k, v in r.items():
            print(k, ":", v)

if __name__ == "__main__":
    run()
