from __future__ import annotations
import pandas as pd
from config.settings import DATA_FILES
from core.data_store import load_table, save_table
from core.validation import validate_table
from services.id_service import generate_id

def add_product(name: str, status: str = "Active") -> dict:
    products = load_table("products")
    new_record = {
        "product_id": generate_id("PROD"),
        "name": name,
        "status": status
    }
    updated = pd.concat([products, pd.DataFrame([new_record])], ignore_index=True)
    clean = validate_table(updated, "products")
    save_table("products", clean)
    return new_record

# === New Products from your pricing plan ===
new_products = [
    "Core Single Class - Drama",
    "Core Single Class - Filmmaking",
    "Core Dual Class (Drama + Filmmaking)",
    "Showreel Package (3 terms)",
    "2-Day Summer Film Shoot",
    "5-Day Summer Film Camp",
    "Ultimate Summer Bundle (Shoot + Camp)",
    "Short Course Full Season Pass",
]

print("Adding new products...\n")
for name in new_products:
    result = add_product(name)
    print(f"✅ Added: {result['name']} ({result['product_id']})")

print("\nDone! New products added successfully.")
