from __future__ import annotations
import pandas as pd
from core.data_store import load_table, save_table
from core.exceptions import ServiceError
from core.validation import validate_table
from services.id_service import generate_id
def link_programme_to_product(programme_id: str, product_id: str) -> dict[str, str]:
    programme_id = programme_id.strip()
    product_id = product_id.strip()
    if not programme_id:
        raise ServiceError("programme_id is required.")
    if not product_id:
        raise ServiceError("product_id is required.")
    links = load_table("programme_products")
    already_exists = (
        (links["programme_id"].astype(str).str.strip() == programme_id)
        & (links["product_id"].astype(str).str.strip() == product_id)
    ).any()
    if already_exists:
        raise ServiceError("This programme-product link already exists.")
    new_record = {
        "programme_product_id": generate_id("PPL"),
        "programme_id": programme_id,
        "product_id": product_id,
    }
    updated = pd.concat([links, pd.DataFrame([new_record])], ignore_index=True)
    clean = validate_table(updated, "programme_products")
    save_table("programme_products", clean)
    return new_record
def link_programme_to_class(programme_id: str, class_id: str) -> dict[str, str]:
    programme_id = programme_id.strip()
    class_id = class_id.strip()
    if not programme_id:
        raise ServiceError("programme_id is required.")
    if not class_id:
        raise ServiceError("class_id is required.")
    links = load_table("programme_classes")
    already_exists = (
        (links["programme_id"].astype(str).str.strip() == programme_id)
        & (links["class_id"].astype(str).str.strip() == class_id)
    ).any()
    if already_exists:
        raise ServiceError("This programme-class link already exists.")
    new_record = {
        "programme_class_id": generate_id("PCL"),
        "programme_id": programme_id,
        "class_id": class_id,
    }
    updated = pd.concat([links, pd.DataFrame([new_record])], ignore_index=True)
    clean = validate_table(updated, "programme_classes")
    save_table("programme_classes", clean)
    return new_record
