from __future__ import annotations
from pathlib import Path
import pandas as pd
IMPORT_DIR = Path("data/import_source")
def inspect_csv(path: Path) -> None:
    print("=" * 100)
    print(f"FILE: {path.name}")
    try:
        df = pd.read_csv(path)
    except Exception as exc:
        print(f"FAILED TO READ: {exc}")
        return
    print(f"ROWS: {len(df)}")
    print(f"COLUMNS ({len(df.columns)}):")
    for col in df.columns:
        print(f"  - {col}")
    print("\nFIRST 3 ROWS:")
    if df.empty:
        print("(empty file)")
    else:
        preview = df.head(3).fillna("").astype(str)
        print(preview.to_string(index=False))
    print()
def main() -> None:
    files = sorted(
        p for p in IMPORT_DIR.iterdir()
        if p.is_file() and p.suffix.lower() == ".csv"
    )
    if not files:
        print("No CSV files found in data/import_source")
        return
    for path in files:
        inspect_csv(path)
if __name__ == "__main__":
    main()
