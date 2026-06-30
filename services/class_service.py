from __future__ import annotations
import pandas as pd
from core.data_store import load_table, save_table
from core.exceptions import ServiceError
from core.upsert import update_rows
from core.validation import validate_table
from services.id_service import generate_id
from services.link_service import link_programme_to_class
VALID_CLASS_STATUSES = {"Active", "Inactive"}
def list_classes() -> pd.DataFrame:
    return load_table("classes")
def create_class(
    name: str,
    programme_id: str = "",
    calendar_id: str = "",
    day: str = "",
    time: str = "",
    status: str = "Active",
) -> dict[str, str]:
    name = name.strip()
    programme_id = programme_id.strip()
    status = status.strip().title()
    if not name:
        raise ServiceError("Class name is required.")
    if status not in VALID_CLASS_STATUSES:
        raise ServiceError(f"Invalid class status: {status}")
    classes = load_table("classes")
    new_record = {
        "class_id": generate_id("CLS"),
        "name": name,
        "programme_id": programme_id,
        "calendar_id": calendar_id.strip(),
        "day": day.strip(),
        "time": time.strip(),
        "status": status,
    }
    updated = pd.concat([classes, pd.DataFrame([new_record])], ignore_index=True)
    clean = validate_table(updated, "classes")
    save_table("classes", clean)
    if programme_id:
        try:
            link_programme_to_class(
                programme_id=programme_id,
                class_id=new_record["class_id"],
            )
        except ServiceError as exc:
            if "already exists" not in str(exc):
                raise
    return new_record
def update_class(
    class_id: str,
    name: str,
    programme_id: str = "",
    calendar_id: str = "",
    day: str = "",
    time: str = "",
    status: str = "Active",
) -> dict[str, str]:
    class_id = class_id.strip()
    name = name.strip()
    programme_id = programme_id.strip()
    status = status.strip().title()
    if not class_id:
        raise ServiceError("class_id is required.")
    if not name:
        raise ServiceError("Class name is required.")
    if status not in VALID_CLASS_STATUSES:
        raise ServiceError(f"Invalid class status: {status}")
    classes = load_table("classes")
    updated = update_rows(
        classes,
        {"class_id": class_id},
        {
            "name": name,
            "programme_id": programme_id,
            "calendar_id": calendar_id.strip(),
            "day": day.strip(),
            "time": time.strip(),
            "status": status,
        },
    )
    clean = validate_table(updated, "classes")
    save_table("classes", clean)
    if programme_id:
        try:
            link_programme_to_class(programme_id=programme_id, class_id=class_id)
        except ServiceError as exc:
            if "already exists" not in str(exc):
                raise
    row = clean[clean["class_id"].astype(str).str.strip() == class_id].iloc[0]
    return row.to_dict()
