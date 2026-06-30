from __future__ import annotations
import pandas as pd
from core.data_store import load_table
from core.exceptions import ServiceError
from services.attendance_service import replace_attendance_for_class_date
from services.roster_service import resolve_class_roster
def build_attendance_register(class_id: str, session_date: str) -> pd.DataFrame:
    class_id = class_id.strip()
    session_date = session_date.strip()
    if not class_id:
        raise ServiceError("class_id is required.")
    if not session_date:
        raise ServiceError("session_date is required.")
    roster = resolve_class_roster(class_id).copy()
    if roster.empty:
        return pd.DataFrame(columns=["student_id", "full_name", "status", "notes"])
    attendance = load_table("attendance")
    existing = attendance[
        (attendance["class_id"].astype(str).str.strip() == class_id)
        & (attendance["session_date"].astype(str).str.strip() == session_date)
    ].copy()
    register = roster.copy()
    if existing.empty:
        register["status"] = "Present"
        register["notes"] = ""
        return register
    status_map = dict(zip(existing["student_id"], existing["status"]))
    notes_map = dict(zip(existing["student_id"], existing["notes"]))
    register["status"] = (
        register["student_id"].map(status_map).fillna("Present")
    )
    register["notes"] = (
        register["student_id"].map(notes_map).fillna("")
    )
    return register
def save_attendance_register(
    class_id: str,
    session_date: str,
    register_rows: list[dict[str, str]],
) -> pd.DataFrame:
    class_id = class_id.strip()
    session_date = session_date.strip()
    if not class_id:
        raise ServiceError("class_id is required.")
    if not session_date:
        raise ServiceError("session_date is required.")
    if not register_rows:
        raise ServiceError("register_rows is required.")
    normalized_rows: list[dict[str, str]] = []
    for row in register_rows:
        normalized_rows.append(
            {
                "student_id": str(row.get("student_id", "")).strip(),
                "status": str(row.get("status", "Present")).strip().title(),
                "notes": str(row.get("notes", "")).strip(),
            }
        )
    return replace_attendance_for_class_date(
        class_id=class_id,
        session_date=session_date,
        rows=normalized_rows,
    )
