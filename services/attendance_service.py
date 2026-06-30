from __future__ import annotations
import pandas as pd
from core.data_store import load_table, save_table
from core.exceptions import ServiceError
from core.upsert import replace_group
from core.validation import validate_table
from services.id_service import generate_id
VALID_ATTENDANCE_STATUSES = {"Present", "Absent", "Late"}
def list_attendance() -> pd.DataFrame:
    return load_table("attendance")
def create_attendance_record(
    student_id: str,
    class_id: str,
    session_date: str,
    status: str = "Present",
    notes: str = "",
) -> dict[str, str]:
    student_id = student_id.strip()
    class_id = class_id.strip()
    session_date = session_date.strip()
    status = status.strip().title()
    if not student_id:
        raise ServiceError("student_id is required.")
    if not class_id:
        raise ServiceError("class_id is required.")
    if not session_date:
        raise ServiceError("session_date is required.")
    if status not in VALID_ATTENDANCE_STATUSES:
        raise ServiceError(f"Invalid attendance status: {status}")
    attendance = load_table("attendance")
    duplicate_mask = (
        (attendance["student_id"].astype(str).str.strip() == student_id)
        & (attendance["class_id"].astype(str).str.strip() == class_id)
        & (attendance["session_date"].astype(str).str.strip() == session_date)
    )
    if duplicate_mask.any():
        raise ServiceError(
            "Attendance record already exists for this student, class, and date."
        )
    new_record = {
        "attendance_id": generate_id("ATT"),
        "student_id": student_id,
        "class_id": class_id,
        "session_date": session_date,
        "status": status,
        "notes": notes.strip(),
    }
    updated = pd.concat([attendance, pd.DataFrame([new_record])], ignore_index=True)
    clean = validate_table(updated, "attendance")
    save_table("attendance", clean)
    return new_record
def replace_attendance_for_class_date(
    class_id: str,
    session_date: str,
    rows: list[dict[str, str]],
) -> pd.DataFrame:
    class_id = class_id.strip()
    session_date = session_date.strip()
    if not class_id:
        raise ServiceError("class_id is required.")
    if not session_date:
        raise ServiceError("session_date is required.")
    if not rows:
        raise ServiceError("At least one attendance row is required.")
    attendance = load_table("attendance")
    new_rows: list[dict[str, str]] = []
    for row in rows:
        student_id = str(row.get("student_id", "")).strip()
        status = str(row.get("status", "Present")).strip().title()
        notes = str(row.get("notes", "")).strip()
        if not student_id:
            raise ServiceError("Every attendance row must include student_id.")
        if status not in VALID_ATTENDANCE_STATUSES:
            raise ServiceError(f"Invalid attendance status: {status}")
        new_rows.append(
            {
                "attendance_id": generate_id("ATT"),
                "student_id": student_id,
                "class_id": class_id,
                "session_date": session_date,
                "status": status,
                "notes": notes,
            }
        )
    rebuilt = replace_group(
        attendance,
        {"class_id": class_id, "session_date": session_date},
        new_rows,
    )
    clean = validate_table(rebuilt, "attendance")
    save_table("attendance", clean)
    return clean[
        (clean["class_id"].astype(str).str.strip() == class_id)
        & (clean["session_date"].astype(str).str.strip() == session_date)
    ].copy()
