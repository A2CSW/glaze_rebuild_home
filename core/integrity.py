from __future__ import annotations
import pandas as pd
from core.exceptions import RecordValidationError
from core.logging_config import get_logger
logger = get_logger(__name__)
def _existing_ids(df: pd.DataFrame, id_column: str) -> set[str]:
    if df.empty or id_column not in df.columns:
        return set()
    return set(df[id_column].fillna("").astype(str).str.strip())
def validate_foreign_keys(table_name: str, df: pd.DataFrame) -> None:
    if df.empty:
        return
    from core.data_store import load_table
    if table_name == "students":
        guardians = load_table("guardians")
        valid_guardian_ids = _existing_ids(guardians, "guardian_id")
        bad_rows = df[
            (df["guardian_id"].astype(str).str.strip() != "")
            & (~df["guardian_id"].astype(str).str.strip().isin(valid_guardian_ids))
        ]
        if not bad_rows.empty:
            raise RecordValidationError(
                "Students reference unknown guardian_id values."
            )
    elif table_name == "products":
        programmes = load_table("programmes")
        valid_programme_ids = _existing_ids(programmes, "programme_id")
        bad_rows = df[
            (df["programme_id"].astype(str).str.strip() != "")
            & (~df["programme_id"].astype(str).str.strip().isin(valid_programme_ids))
        ]
        if not bad_rows.empty:
            raise RecordValidationError(
                "Products reference unknown programme_id values."
            )
    elif table_name == "programme_products":
        programmes = load_table("programmes")
        products = load_table("products")
        valid_programme_ids = _existing_ids(programmes, "programme_id")
        valid_product_ids = _existing_ids(products, "product_id")
        bad_rows = df[
            (~df["programme_id"].astype(str).str.strip().isin(valid_programme_ids))
            | (~df["product_id"].astype(str).str.strip().isin(valid_product_ids))
        ]
        if not bad_rows.empty:
            raise RecordValidationError(
                "Programme-product links reference unknown IDs."
            )
    elif table_name == "programme_classes":
        programmes = load_table("programmes")
        classes = load_table("classes")
        valid_programme_ids = _existing_ids(programmes, "programme_id")
        valid_class_ids = _existing_ids(classes, "class_id")
        bad_rows = df[
            (~df["programme_id"].astype(str).str.strip().isin(valid_programme_ids))
            | (~df["class_id"].astype(str).str.strip().isin(valid_class_ids))
        ]
        if not bad_rows.empty:
            raise RecordValidationError(
                "Programme-class links reference unknown IDs."
            )
    elif table_name == "enrolments":
        students = load_table("students")
        products = load_table("products")
        valid_student_ids = _existing_ids(students, "student_id")
        valid_product_ids = _existing_ids(products, "product_id")
        bad_rows = df[
            (~df["student_id"].astype(str).str.strip().isin(valid_student_ids))
            | (~df["product_id"].astype(str).str.strip().isin(valid_product_ids))
        ]
        if not bad_rows.empty:
            raise RecordValidationError(
                "Enrolments reference unknown student_id or product_id values."
            )
    elif table_name == "attendance":
        students = load_table("students")
        classes = load_table("classes")
        valid_student_ids = _existing_ids(students, "student_id")
        valid_class_ids = _existing_ids(classes, "class_id")
        bad_rows = df[
            (~df["student_id"].astype(str).str.strip().isin(valid_student_ids))
            | (~df["class_id"].astype(str).str.strip().isin(valid_class_ids))
        ]
        if not bad_rows.empty:
            raise RecordValidationError(
                "Attendance references unknown student_id or class_id values."
            )
    elif table_name == "payment_aliases":
        guardians = load_table("guardians")
        students = load_table("students")
        valid_guardian_ids = _existing_ids(guardians, "guardian_id")
        valid_student_ids = _existing_ids(students, "student_id")
        bad_rows = df[
            (~df["guardian_id"].astype(str).str.strip().isin(valid_guardian_ids))
            | (
                (df["student_id"].astype(str).str.strip() != "")
                & (~df["student_id"].astype(str).str.strip().isin(valid_student_ids))
            )
        ]
        if not bad_rows.empty:
            raise RecordValidationError(
                "Payment aliases reference unknown guardian_id or student_id values."
            )
    elif table_name == "bank_transactions":
        students = load_table("students")
        guardians = load_table("guardians")
        valid_student_ids = _existing_ids(students, "student_id")
        valid_guardian_ids = _existing_ids(guardians, "guardian_id")
        bad_rows = df[
            (
                (df["matched_student_id"].astype(str).str.strip() != "")
                & (~df["matched_student_id"].astype(str).str.strip().isin(valid_student_ids))
            )
            | (
                (df["matched_guardian_id"].astype(str).str.strip() != "")
                & (~df["matched_guardian_id"].astype(str).str.strip().isin(valid_guardian_ids))
            )
        ]
        if not bad_rows.empty:
            raise RecordValidationError(
                "Bank transactions reference unknown matched student or guardian IDs."
            )
