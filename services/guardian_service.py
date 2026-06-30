from __future__ import annotations
import pandas as pd
from core.data_store import load_table, save_table
from core.exceptions import ServiceError
from core.upsert import update_rows
from core.validation import validate_table
from services.id_service import generate_id
def list_guardians() -> pd.DataFrame:
    return load_table("guardians")
def create_guardian(
    guardian_name: str,
    email: str = "",
    phone: str = "",
    notes: str = "",
) -> dict[str, str]:
    guardian_name = guardian_name.strip()
    if not guardian_name:
        raise ServiceError("Guardian name is required.")
    guardians = load_table("guardians")
    new_record = {
        "guardian_id": generate_id("GDN"),
        "guardian_name": guardian_name,
        "email": email.strip(),
        "phone": phone.strip(),
        "notes": notes.strip(),
    }
    updated = pd.concat([guardians, pd.DataFrame([new_record])], ignore_index=True)
    clean = validate_table(updated, "guardians")
    save_table("guardians", clean)
    return new_record
def update_guardian(
    guardian_id: str,
    guardian_name: str,
    email: str = "",
    phone: str = "",
    notes: str = "",
) -> dict[str, str]:
    guardian_id = guardian_id.strip()
    guardian_name = guardian_name.strip()
    if not guardian_id:
        raise ServiceError("guardian_id is required.")
    if not guardian_name:
        raise ServiceError("Guardian name is required.")
    guardians = load_table("guardians")
    updated = update_rows(
        guardians,
        {"guardian_id": guardian_id},
        {
            "guardian_name": guardian_name,
            "email": email.strip(),
            "phone": phone.strip(),
            "notes": notes.strip(),
        },
    )
    clean = validate_table(updated, "guardians")
    save_table("guardians", clean)
    row = clean[clean["guardian_id"].astype(str).str.strip() == guardian_id].iloc[0]
    return row.to_dict()
