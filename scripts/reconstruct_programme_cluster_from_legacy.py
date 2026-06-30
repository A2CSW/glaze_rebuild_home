from __future__ import annotations
from pathlib import Path
import hashlib
import pandas as pd
from config.settings import ensure_directories
from core.atomic_io import atomic_write_csv
IMPORT_DIR = Path("data/import_source")
PREVIEW_DIR = Path("data/raw/migration_preview")
def load_csv(filename: str) -> pd.DataFrame:
    return pd.read_csv(IMPORT_DIR / filename).fillna("")
def clean_text(value: str) -> str:
    return str(value).strip()
def make_id(prefix: str, text: str) -> str:
    digest = hashlib.md5(text.strip().lower().encode("utf-8")).hexdigest()[:8].upper()
    return f"{prefix}-{digest}"
def normalize_student_status(value: str) -> str:
    text = clean_text(value).title()
    if not text:
        return "Inactive"
    return text
def normalize_enrolment_status(student_status: str) -> str:
    text = normalize_student_status(student_status)
    if text == "Current":
        return "Active"
    if text == "Former":
        return "Completed"
    if text == "Taster":
        return "Pending"
    return "Inactive"
def build_programmes(students_df: pd.DataFrame) -> pd.DataFrame:
    names = sorted({
        clean_text(v)
        for v in students_df.get("cohort", pd.Series(dtype=str)).tolist()
        if clean_text(v)
    })
    rows = []
    for name in names:
        rows.append(
            {
                "programme_id": make_id("PRG", f"cohort::{name}"),
                "name": name,
                "status": "Active",
                "notes": "Reconstructed from legacy cohort field",
            }
        )
    return pd.DataFrame(rows, columns=["programme_id", "name", "status", "notes"])
def build_products(students_df: pd.DataFrame, programmes_df: pd.DataFrame) -> pd.DataFrame:
    programme_lookup = {
        row["name"]: row["programme_id"]
        for _, row in programmes_df.iterrows()
    }
    keys = sorted({
        (
            clean_text(row.get("membership_type", "")),
            clean_text(row.get("cohort", "")),
        )
        for _, row in students_df.iterrows()
        if clean_text(row.get("membership_type", "")) or clean_text(row.get("cohort", ""))
    })
    rows = []
    for membership_type, cohort in keys:
        if membership_type and cohort:
            name = f"{membership_type} - {cohort}"
        elif membership_type:
            name = membership_type
        else:
            name = cohort
        programme_id = programme_lookup.get(cohort, "")
        rows.append(
            {
                "product_id": make_id("PROD", f"{membership_type}|{cohort}|{name}"),
                "name": name,
                "programme_id": programme_id,
                "status": "Active",
            }
        )
    return pd.DataFrame(rows, columns=["product_id", "name", "programme_id", "status"])
def build_programme_products(products_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in products_df.iterrows():
        programme_id = clean_text(row.get("programme_id", ""))
        product_id = clean_text(row.get("product_id", ""))
        if not programme_id or not product_id:
            continue
        rows.append(
            {
                "programme_product_id": make_id("PPL", f"{programme_id}|{product_id}"),
                "programme_id": programme_id,
                "product_id": product_id,
            }
        )
    return pd.DataFrame(rows, columns=["programme_product_id", "programme_id", "product_id"])
def infer_programme_name_from_class_name(class_name: str) -> str:
    text = class_name.lower()
    if any(token in text for token in ["4-8", "(4-8)", "4-8s"]):
        return "Littlies"
    if any(token in text for token in ["8-12", "8-12s", "10-13", "10-13s"]):
        return "Middlies"
    if any(token in text for token in ["11-16", "13-17", "13-17s"]):
        return "Oldies"
    return ""
def build_classes(attendance_df: pd.DataFrame, programmes_df: pd.DataFrame) -> pd.DataFrame:
    programme_lookup = {
        row["name"]: row["programme_id"]
        for _, row in programmes_df.iterrows()
    }
    raw_classes = set()
    if "classes" in attendance_df.columns:
        for value in attendance_df["classes"].tolist():
            text = clean_text(value)
            if not text:
                continue
            if text.lower() in {"nan", "nan | nan"}:
                continue
            parts = [p.strip() for p in text.split("|") if p.strip()]
            for part in parts:
                if not part or part.lower() == "nan":
                    continue
                raw_classes.add(part)
    rows = []
    for class_name in sorted(raw_classes):
        inferred_programme_name = infer_programme_name_from_class_name(class_name)
        matched_programme_id = programme_lookup.get(inferred_programme_name, "")
        rows.append(
            {
                "class_id": make_id("CLS", class_name),
                "name": class_name,
                "programme_id": matched_programme_id,
                "calendar_id": "",
                "day": "",
                "time": "",
                "status": "Active",
            }
        )
    return pd.DataFrame(
        rows,
        columns=["class_id", "name", "programme_id", "calendar_id", "day", "time", "status"],
    )
def build_programme_classes(classes_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in classes_df.iterrows():
        programme_id = clean_text(row.get("programme_id", ""))
        class_id = clean_text(row.get("class_id", ""))
        if not programme_id or not class_id:
            continue
        rows.append(
            {
                "programme_class_id": make_id("PCL", f"{programme_id}|{class_id}"),
                "programme_id": programme_id,
                "class_id": class_id,
            }
        )
    return pd.DataFrame(rows, columns=["programme_class_id", "programme_id", "class_id"])
def build_enrolments(students_df: pd.DataFrame, products_df: pd.DataFrame) -> pd.DataFrame:
    products_by_name = {
        clean_text(row.get("name", "")): clean_text(row.get("product_id", ""))
        for _, row in products_df.iterrows()
    }
    rows = []
    for _, row in students_df.iterrows():
        student_id = clean_text(row.get("student_id", ""))
        membership_type = clean_text(row.get("membership_type", ""))
        cohort = clean_text(row.get("cohort", ""))
        student_status = clean_text(row.get("status", ""))
        if not student_id:
            continue
        candidate_product_name = ""
        if membership_type and cohort:
            candidate_product_name = f"{membership_type} - {cohort}"
        elif membership_type:
            candidate_product_name = membership_type
        elif cohort:
            candidate_product_name = cohort
        product_id = products_by_name.get(candidate_product_name, "")
        if not product_id:
            continue
        rows.append(
            {
                "enrolment_id": make_id("ENR", f"{student_id}|{product_id}"),
                "student_id": student_id,
                "product_id": product_id,
                "start_date": "",
                "end_date": "",
                "enrolment_status": normalize_enrolment_status(student_status),
            }
        )
    return pd.DataFrame(
        rows,
        columns=["enrolment_id", "student_id", "product_id", "start_date", "end_date", "enrolment_status"],
    )
def main() -> None:
    ensure_directories()
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    students_master = load_csv("1_students_master copy.csv")
    attendance_summary = load_csv("3_attendance_tracker copy.csv")
    programmes = build_programmes(students_master)
    products = build_products(students_master, programmes)
    programme_products = build_programme_products(products)
    classes = build_classes(attendance_summary, programmes)
    programme_classes = build_programme_classes(classes)
    enrolments = build_enrolments(students_master, products)
    atomic_write_csv(programmes, PREVIEW_DIR / "programmes_preview.csv")
    atomic_write_csv(products, PREVIEW_DIR / "products_preview.csv")
    atomic_write_csv(programme_products, PREVIEW_DIR / "programme_products_preview.csv")
    atomic_write_csv(classes, PREVIEW_DIR / "classes_preview.csv")
    atomic_write_csv(programme_classes, PREVIEW_DIR / "programme_classes_preview.csv")
    atomic_write_csv(enrolments, PREVIEW_DIR / "enrolments_preview.csv")
    print("Preview reconstruction complete.")
    print(f"Programmes preview rows: {len(programmes)}")
    print(f"Products preview rows: {len(products)}")
    print(f"Programme-products preview rows: {len(programme_products)}")
    print(f"Classes preview rows: {len(classes)}")
    print(f"Programme-classes preview rows: {len(programme_classes)}")
    print(f"Enrolments preview rows: {len(enrolments)}")
if __name__ == "__main__":
    main()
