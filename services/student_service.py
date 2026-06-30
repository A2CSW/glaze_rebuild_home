from __future__ import annotations
import pandas as pd
from core.data_store import load_table, save_table
from core.exceptions import ServiceError
from core.upsert import update_rows
from core.validation import validate_table
from services.id_service import generate_id
VALID_STUDENT_STATUSES = {"Current", "Former", "Taster", "Inactive"}
def build_full_name(first_name: str, last_name: str) -> str:
    return f"{first_name.strip()} {last_name.strip()}".strip()
def list_students() -> pd.DataFrame:
    return load_table("students")
def create_student(
    first_name: str,
    last_name: str,
    status: str = "Current",
    guardian_id: str = "",
    date_of_birth: str = "",
    search_rule: str = "",
    notes: str = "",
) -> dict[str, str]:
    first_name = first_name.strip()
    last_name = last_name.strip()
    status = status.strip().title()
    if not first_name:
        raise ServiceError("First name is required.")
    if not last_name:
        raise ServiceError("Last name is required.")
    if status not in VALID_STUDENT_STATUSES:
        raise ServiceError(f"Invalid student status: {status}")
    students = load_table("students")
    new_record = {
        "student_id": generate_id("STU"),
        "first_name": first_name,
        "last_name": last_name,
        "full_name": build_full_name(first_name, last_name),
        "date_of_birth": date_of_birth.strip(),
        "status": status,
        "guardian_id": guardian_id.strip(),
        "search_rule": search_rule.strip(),
        "notes": notes.strip(),
    }
    updated = pd.concat([students, pd.DataFrame([new_record])], ignore_index=True)
    clean = validate_table(updated, "students")
    save_table("students", clean)
    return new_record
def update_student(
    student_id: str,
    first_name: str,
    last_name: str,
    status: str,
    guardian_id: str = "",
    date_of_birth: str = "",
    search_rule: str = "",
    notes: str = "",
) -> dict[str, str]:
    student_id = student_id.strip()
    first_name = first_name.strip()
    last_name = last_name.strip()
    status = status.strip().title()
    if not student_id:
        raise ServiceError("student_id is required.")
    if not first_name:
        raise ServiceError("First name is required.")
    if not last_name:
        raise ServiceError("Last name is required.")
    if status not in VALID_STUDENT_STATUSES:
        raise ServiceError(f"Invalid student status: {status}")
    students = load_table("students")
    updated = update_rows(
        students,
        {"student_id": student_id},
        {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": build_full_name(first_name, last_name),
            "date_of_birth": date_of_birth.strip(),
            "status": status,
            "guardian_id": guardian_id.strip(),
            "search_rule": search_rule.strip(),
            "notes": notes.strip(),
        },
    )
    clean = validate_table(updated, "students")
    save_table("students", clean)
    row = clean[clean["student_id"].astype(str).str.strip() == student_id].iloc[0]
    return row.to_dict()
