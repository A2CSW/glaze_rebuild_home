from __future__ import annotations
import pandas as pd
from core.data_store import load_table, save_table
from core.exceptions import ServiceError
from core.upsert import update_rows
from core.validation import validate_table
from services.id_service import generate_id
VALID_PRODUCT_STATUSES = {"Active", "Inactive", "Draft"}
def list_products() -> pd.DataFrame:
    return load_table("products")
def create_product(
    name: str,
    programme_id: str = "",
    status: str = "Active",
) -> dict[str, str]:
    name = name.strip()
    status = status.strip().title()
    if not name:
        raise ServiceError("Product name is required.")
    if status not in VALID_PRODUCT_STATUSES:
        raise ServiceError(f"Invalid product status: {status}")
    products = load_table("products")
    new_record = {
        "product_id": generate_id("PROD"),
        "name": name,
        "programme_id": programme_id.strip(),
        "status": status,
    }
    updated = pd.concat([products, pd.DataFrame([new_record])], ignore_index=True)
    clean = validate_table(updated, "products")
    save_table("products", clean)
    return new_record
def update_product(
    product_id: str,
    name: str,
    programme_id: str = "",
    status: str = "Active",
) -> dict[str, str]:
    product_id = product_id.strip()
    name = name.strip()
    programme_id = programme_id.strip()
    status = status.strip().title()
    if not product_id:
        raise ServiceError("product_id is required.")
    if not name:
        raise ServiceError("Product name is required.")
    if status not in VALID_PRODUCT_STATUSES:
        raise ServiceError(f"Invalid product status: {status}")
    products = load_table("products")
    updated = update_rows(
        products,
        {"product_id": product_id},
        {
            "name": name,
            "programme_id": programme_id,
            "status": status,
        },
    )
    clean = validate_table(updated, "products")
    save_table("products", clean)
    row = clean[clean["product_id"].astype(str).str.strip() == product_id].iloc[0]
    return row.to_dict()
