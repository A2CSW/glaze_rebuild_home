from __future__ import annotations
import pandas as pd
from core.data_store import load_table, save_table
from core.exceptions import ServiceError
from core.upsert import update_rows
from core.validation import validate_table
from services.id_service import generate_id
VALID_PROGRAMME_STATUSES = {"Active", "Inactive", "Draft"}
def list_programmes() -> pd.DataFrame:
    return load_table("programmes")
def create_programme(
    name: str,
    status: str = "Active",
    notes: str = "",
) -> dict[str, str]:
    name = name.strip()
    status = status.strip().title()
    if not name:
        raise ServiceError("Programme name is required.")
    if status not in VALID_PROGRAMME_STATUSES:
        raise ServiceError(f"Invalid programme status: {status}")
    programmes = load_table("programmes")
    new_record = {
        "programme_id": generate_id("PRG"),
        "name": name,
        "status": status,
        "notes": notes.strip(),
    }
    updated = pd.concat([programmes, pd.DataFrame([new_record])], ignore_index=True)
    clean = validate_table(updated, "programmes")
    save_table("programmes", clean)
    return new_record
def update_programme(
    programme_id: str,
    name: str,
    status: str,
    notes: str = "",
) -> dict[str, str]:
    programme_id = programme_id.strip()
    name = name.strip()
    status = status.strip().title()
    if not programme_id:
        raise ServiceError("programme_id is required.")
    if not name:
        raise ServiceError("Programme name is required.")
    if status not in VALID_PROGRAMME_STATUSES:
        raise ServiceError(f"Invalid programme status: {status}")
    programmes = load_table("programmes")
    updated = update_rows(
        programmes,
        {"programme_id": programme_id},
        {
            "name": name,
            "status": status,
            "notes": notes.strip(),
        },
    )
    clean = validate_table(updated, "programmes")
    save_table("programmes", clean)
    row = clean[clean["programme_id"].astype(str).str.strip() == programme_id].iloc[0]
    return row.to_dict()
