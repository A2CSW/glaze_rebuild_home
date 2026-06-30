from __future__ import annotations
from pathlib import Path
import hashlib
import pandas as pd
from config.settings import ensure_directories
from core.atomic_io import atomic_write_csv
from core.logging_config import get_logger
logger = get_logger(__name__)
IMPORT_DIR = Path("data/import_source")
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
def make_guardian_id(name: str, mobile: str, email: str) -> str:
    base = f"{name.strip().lower()}|{mobile.strip()}|{email.strip().lower()}"
    digest = hashlib.md5(base.encode("utf-8")).hexdigest()[:8].upper()
    return f"GDN-{digest}"
def split_full_name(full_name: str) -> tuple[str, str]:
    parts = str(full_name).strip().split()
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])
def normalize_status(value: str) -> str:
    text = str(value).strip().title()
    if not text:
        return "Inactive"
    return text
def load_csv(filename: str) -> pd.DataFrame:
    path = IMPORT_DIR / filename
    return pd.read_csv(path).fillna("")
def build_guardians_df(contacts_df: pd.DataFrame) -> pd.DataFrame:
    guardian_rows: list[dict[str, str]] = []
    for _, row in contacts_df.iterrows():
        for slot in [1, 2]:
            name = str(row.get(f"guardian_{slot}_name", "")).strip()
            mobile = str(row.get(f"guardian_{slot}_mobile", "")).strip()
            email = str(row.get(f"guardian_{slot}_email", "")).strip()
            if not name:
                continue
            guardian_rows.append(
                {
                    "guardian_id": make_guardian_id(name, mobile, email),
                    "guardian_name": name,
                    "email": email,
                    "phone": mobile,
                    "notes": "",
                }
            )
    if not guardian_rows:
        return pd.DataFrame(columns=["guardian_id", "guardian_name", "email", "phone", "notes"])
    guardians = pd.DataFrame(guardian_rows).drop_duplicates(
        subset=["guardian_id"]
    ).sort_values(by=["guardian_name", "guardian_id"]).reset_index(drop=True)
    return guardians
def build_students_df(
    students_master_df: pd.DataFrame,
    contacts_df: pd.DataFrame,
) -> pd.DataFrame:
    contact_lookup = contacts_df.set_index("student_id").to_dict(orient="index")
    rows: list[dict[str, str]] = []
    for _, row in students_master_df.iterrows():
        student_id = str(row.get("student_id", "")).strip()
        full_name = str(row.get("full_name", "")).strip()
        dob = str(row.get("dob", "")).strip()
        status = normalize_status(row.get("status", ""))
        search_rule = str(row.get("search_rule", "")).strip()
        if not student_id:
            continue
        first_name, last_name = split_full_name(full_name)
        contact_row = contact_lookup.get(student_id, {})
        g1_name = str(contact_row.get("guardian_1_name", "")).strip()
        g1_mobile = str(contact_row.get("guardian_1_mobile", "")).strip()
        g1_email = str(contact_row.get("guardian_1_email", "")).strip()
        guardian_id = ""
        if g1_name:
            guardian_id = make_guardian_id(g1_name, g1_mobile, g1_email)
        rows.append(
            {
                "student_id": student_id,
                "first_name": first_name,
                "last_name": last_name,
                "full_name": full_name,
                "date_of_birth": dob,
                "status": status,
                "guardian_id": guardian_id,
                "search_rule": search_rule,
                "notes": "",
            }
        )
    students = pd.DataFrame(rows).drop_duplicates(
        subset=["student_id"]
    ).sort_values(by=["student_id"]).reset_index(drop=True)
    return students
def save_sidecar(df: pd.DataFrame, filename: str) -> None:
    path = RAW_DIR / filename
    atomic_write_csv(df, path)
    logger.info("Saved sidecar snapshot: %s", path)
def main() -> None:
    ensure_directories()
    students_master = load_csv("1_students_master copy.csv")
    contacts = load_csv("5_students_contacts copy.csv")
    medical = load_csv("4_medical_and_permissions copy.csv")
    payments = load_csv("2_payments_master copy.csv")
    attendance_summary = load_csv("3_attendance_tracker copy.csv")
    guardians = build_guardians_df(contacts)
    students = build_students_df(students_master, contacts)
    atomic_write_csv(guardians, PROCESSED_DIR / "guardians.csv")
    atomic_write_csv(students, PROCESSED_DIR / "students.csv")
    save_sidecar(medical, "legacy_medical_snapshot.csv")
    save_sidecar(payments, "legacy_payments_snapshot.csv")
    save_sidecar(attendance_summary, "legacy_attendance_summary.csv")
    save_sidecar(contacts, "legacy_contacts_snapshot.csv")
    save_sidecar(students_master, "legacy_students_master_snapshot.csv")
    print("Migration complete.")
    print(f"Students migrated: {len(students)}")
    print(f"Guardians migrated: {len(guardians)}")
    print("Sidecar snapshots saved in data/raw/")
if __name__ == "__main__":
    main()
