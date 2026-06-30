from __future__ import annotations
import pandas as pd
from pathlib import Path
from typing import Any
from datetime import datetime
from config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR
from core.exceptions import ServiceError
from core.data_store import save_table
from services.guardian_service import create_guardian
from services.student_service import create_student
from services.id_service import generate_id   # for audit id if needed

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower().str.replace(r"[^\w\s]", "", regex=True).str.replace(r"\s+", "_", regex=True)
    return df

def _get_value(row: pd.Series, *names: str, default: str = "") -> str:
    for name in names:
        if name in row and pd.notna(row[name]):
            return str(row[name]).strip()
    return default

def ingest_form(csv_path: str | Path, form_type: str = "auto") -> dict[str, Any]:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Form file not found: {path}")

    df = pd.read_csv(path)
    df = _normalize_columns(df)

    if form_type == "auto":
        cols = set(df.columns)
        if "childs_name" in cols or "taster_class" in cols:
            form_type = "taster"
        elif "how_many_children_are_you_enrolling" in cols:
            form_type = "enrolment"
        elif "are_you_happy_for_us_to_make_audio" in cols:
            form_type = "consent"
        else:
            form_type = "contact"

    results = {
        "form_type": form_type,
        "total_rows": len(df),
        "guardians_created": 0,
        "students_created": 0,
        "errors": [],
        "source_file": path.name,
    }

    for idx, row in df.iterrows():
        try:
            # Guardian
            guardian_name = _get_value(row, "name", "parent_full_name", "parentguardian_name", "guardian_name")
            email = _get_value(row, "email_address", "email", "parent_email")
            phone = _get_value(row, "mobile_number", "mobile", "parent_mobile_number")

            guardian_id = ""
            if guardian_name:
                guardian = create_guardian(
                    guardian_name=guardian_name,
                    email=email,
                    phone=phone,
                    notes=f"Imported from {form_type} form | source: {path.name}"
                )
                guardian_id = guardian["guardian_id"]
                results["guardians_created"] += 1

            # Student
            if form_type in ("taster", "enrolment"):
                child_name = _get_value(row, "childs_name", "child_name", "student_name")
                if not child_name and form_type == "enrolment":
                    child_name = f"Child {idx+1}"

                if child_name:
                    parts = child_name.split(maxsplit=1)
                    first = parts[0]
                    last = parts[1] if len(parts) > 1 else "Placeholder"

                    create_student(
                        first_name=first,
                        last_name=last,
                        status="Taster" if form_type == "taster" else "Current",
                        guardian_id=guardian_id,
                        date_of_birth=_get_value(row, "child_date_of_birth"),
                        search_rule="",
                        notes=f"Imported from {form_type} | source: {path.name}"
                    )
                    results["students_created"] += 1

        except Exception as e:
            results["errors"].append(f"Row {idx}: {str(e)}")

    # Archive with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"archived_{form_type}_{timestamp}_{path.name}"
    path.rename(PROCESSED_DATA_DIR / archive_name)
    results["archived_as"] = archive_name

    return results
