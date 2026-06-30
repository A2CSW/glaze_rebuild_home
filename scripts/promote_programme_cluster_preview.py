from __future__ import annotations
from pathlib import Path
from core.atomic_io import safe_read_csv
from core.data_store import save_table
PREVIEW_DIR = Path("data/raw/migration_preview")
def main() -> None:
    mapping = {
        "programmes_preview.csv": "programmes",
        "products_preview.csv": "products",
        "programme_products_preview.csv": "programme_products",
        "classes_preview.csv": "classes",
        "programme_classes_preview.csv": "programme_classes",
        "enrolments_preview.csv": "enrolments",
    }
    for filename, table_name in mapping.items():
        path = PREVIEW_DIR / filename
        df = safe_read_csv(path)
        save_table(table_name, df)
        print(f"Promoted {filename} -> {table_name} ({len(df)} rows)")
    print("Programme cluster preview promoted successfully.")
if __name__ == "__main__":
    main()
