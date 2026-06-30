from __future__ import annotations
from pathlib import Path
import hashlib
import pandas as pd
from config.settings import ensure_directories
from core.atomic_io import atomic_write_csv
PREVIEW_DIR = Path("data/raw/migration_preview")
def make_id(prefix: str, text: str) -> str:
    digest = hashlib.md5(text.strip().lower().encode("utf-8")).hexdigest()[:8].upper()
    return f"{prefix}-{digest}"
def build_programmes() -> pd.DataFrame:
    names = ["Drama", "Filmmaking", "Art4Film", "Stopmo"]
    rows = [
        {
            "programme_id": make_id("PRG", name),
            "name": name,
            "status": "Active",
            "notes": "Canonical seeded programme",
        }
        for name in names
    ]
    return pd.DataFrame(rows, columns=["programme_id", "name", "status", "notes"])
def build_products(programmes_df: pd.DataFrame) -> pd.DataFrame:
    programme_lookup = {
        row["name"]: row["programme_id"]
        for _, row in programmes_df.iterrows()
    }
    rows = [
        {"name": "Drama Membership", "programme_name": "Drama"},
        {"name": "Filmmaking Membership", "programme_name": "Filmmaking"},
        {"name": "Dual Membership", "programme_name": ""},
        {"name": "Showreel Package", "programme_name": ""},
        {"name": "Summer Shoot", "programme_name": ""},
        {"name": "Art4Film Term Pass", "programme_name": "Art4Film"},
        {"name": "Stopmo Term Pass", "programme_name": "Stopmo"},
        {"name": "Full Season Pass", "programme_name": ""},
        {"name": "Summer Camp Member", "programme_name": ""},
        {"name": "Summer Camp Non-Member", "programme_name": ""},
        {"name": "Ultimate Summer Pass", "programme_name": ""},
    ]
    built = []
    for row in rows:
        name = row["name"]
        programme_name = row["programme_name"]
        built.append(
            {
                "product_id": make_id("PROD", name),
                "name": name,
                "programme_id": programme_lookup.get(programme_name, ""),
                "status": "Active",
            }
        )
    return pd.DataFrame(built, columns=["product_id", "name", "programme_id", "status"])
def build_programme_products(programmes_df: pd.DataFrame, products_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, product in products_df.iterrows():
        programme_id = str(product.get("programme_id", "")).strip()
        product_id = str(product.get("product_id", "")).strip()
        if not programme_id:
            continue
        rows.append(
            {
                "programme_product_id": make_id("PPL", f"{programme_id}|{product_id}"),
                "programme_id": programme_id,
                "product_id": product_id,
            }
        )
    return pd.DataFrame(rows, columns=["programme_product_id", "programme_id", "product_id"])
def main() -> None:
    ensure_directories()
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    programmes = build_programmes()
    products = build_products(programmes)
    programme_products = build_programme_products(programmes, products)
    atomic_write_csv(programmes, PREVIEW_DIR / "canonical_programmes_preview.csv")
    atomic_write_csv(products, PREVIEW_DIR / "canonical_products_preview.csv")
    atomic_write_csv(programme_products, PREVIEW_DIR / "canonical_programme_products_preview.csv")
    print("Canonical catalogue preview built.")
    print(f"Programmes preview rows: {len(programmes)}")
    print(f"Products preview rows: {len(products)}")
    print(f"Programme-products preview rows: {len(programme_products)}")
if __name__ == "__main__":
    main()
