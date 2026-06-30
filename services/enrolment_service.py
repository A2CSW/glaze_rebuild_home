from __future__ import annotations
import pandas as pd
from core.data_store import load_table, save_table
from core.exceptions import ServiceError
from core.upsert import update_rows
from core.validation import validate_table
from services.id_service import generate_id
VALID_ENROLMENT_STATUSES = {"Active", "Inactive", "Cancelled", "Completed", "Pending"}
def list_enrolments() -> pd.DataFrame:
    return load_table("enrolments")
def create_enrolment(
    student_id: str,
    product_id: str,
    start_date: str = "",
    end_date: str = "",
    enrolment_status: str = "Active",
) -> dict[str, str]:
    student_id = student_id.strip()
    product_id = product_id.strip()
    enrolment_status = enrolment_status.strip().title()
    if not student_id:
        raise ServiceError("student_id is required.")
    if not product_id:
        raise ServiceError("product_id is required.")
    if enrolment_status not in VALID_ENROLMENT_STATUSES:
        raise ServiceError(f"Invalid enrolment status: {enrolment_status}")
    enrolments = load_table("enrolments")
    new_record = {
        "enrolment_id": generate_id("ENR"),
        "student_id": student_id,
        "product_id": product_id,
        "start_date": start_date.strip(),
        "end_date": end_date.strip(),
        "enrolment_status": enrolment_status,
    }
    updated = pd.concat([enrolments, pd.DataFrame([new_record])], ignore_index=True)
    clean = validate_table(updated, "enrolments")
    save_table("enrolments", clean)
    return new_record
def update_enrolment(
    enrolment_id: str,
    student_id: str,
    product_id: str,
    start_date: str = "",
    end_date: str = "",
    enrolment_status: str = "Active",
) -> dict[str, str]:
    enrolment_id = enrolment_id.strip()
    student_id = student_id.strip()
    product_id = product_id.strip()
    enrolment_status = enrolment_status.strip().title()
    if not enrolment_id:
        raise ServiceError("enrolment_id is required.")
    if not student_id:
        raise ServiceError("student_id is required.")
    if not product_id:
        raise ServiceError("product_id is required.")
    if enrolment_status not in VALID_ENROLMENT_STATUSES:
        raise ServiceError(f"Invalid enrolment status: {enrolment_status}")
    enrolments = load_table("enrolments")
    updated = update_rows(
        enrolments,
        {"enrolment_id": enrolment_id},
        {
            "student_id": student_id,
            "product_id": product_id,
            "start_date": start_date.strip(),
            "end_date": end_date.strip(),
            "enrolment_status": enrolment_status,
        },
    )
    clean = validate_table(updated, "enrolments")
    save_table("enrolments", clean)
    row = clean[clean["enrolment_id"].astype(str).str.strip() == enrolment_id].iloc[0]
    return row.to_dict()
