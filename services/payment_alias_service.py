from __future__ import annotations
import pandas as pd
from core.data_store import load_table, save_table
from core.exceptions import ServiceError
from core.upsert import update_rows
from core.validation import validate_table
from services.id_service import generate_id
def list_payment_aliases() -> pd.DataFrame:
    return load_table("payment_aliases")
def create_payment_alias(
    guardian_id: str,
    alias: str,
    student_id: str = "",
    notes: str = "",
) -> dict[str, str]:
    guardian_id = guardian_id.strip()
    alias = alias.strip()
    student_id = student_id.strip()
    if not guardian_id:
        raise ServiceError("guardian_id is required.")
    if not alias:
        raise ServiceError("Alias is required.")
    aliases = load_table("payment_aliases")
    new_record = {
        "alias_id": generate_id("ALS"),
        "guardian_id": guardian_id,
        "student_id": student_id,
        "alias": alias,
        "notes": notes.strip(),
    }
    updated = pd.concat([aliases, pd.DataFrame([new_record])], ignore_index=True)
    clean = validate_table(updated, "payment_aliases")
    save_table("payment_aliases", clean)
    return new_record
def update_payment_alias(
    alias_id: str,
    guardian_id: str,
    alias: str,
    student_id: str = "",
    notes: str = "",
) -> dict[str, str]:
    alias_id = alias_id.strip()
    guardian_id = guardian_id.strip()
    alias = alias.strip()
    student_id = student_id.strip()
    if not alias_id:
        raise ServiceError("alias_id is required.")
    if not guardian_id:
        raise ServiceError("guardian_id is required.")
    if not alias:
        raise ServiceError("Alias is required.")
    aliases = load_table("payment_aliases")
    updated = update_rows(
        aliases,
        {"alias_id": alias_id},
        {
            "guardian_id": guardian_id,
            "student_id": student_id,
            "alias": alias,
            "notes": notes.strip(),
        },
    )
    clean = validate_table(updated, "payment_aliases")
    save_table("payment_aliases", clean)
    row = clean[clean["alias_id"].astype(str).str.strip() == alias_id].iloc[0]
    return row.to_dict()
