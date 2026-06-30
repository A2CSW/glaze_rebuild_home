from __future__ import annotations
import pandas as pd
from core.data_store import load_table
def get_students_view() -> pd.DataFrame:
    students = load_table("students").copy()
    if students.empty:
        return students
    if "full_name" not in students.columns:
        students["full_name"] = (
            students["first_name"].fillna("").astype(str).str.strip()
            + " "
            + students["last_name"].fillna("").astype(str).str.strip()
        ).str.strip()
    return students.sort_values(by=["full_name", "student_id"]).reset_index(drop=True)
def get_guardians_view() -> pd.DataFrame:
    guardians = load_table("guardians").copy()
    if guardians.empty:
        return guardians
    return guardians.sort_values(by=["guardian_name", "guardian_id"]).reset_index(drop=True)
def get_classes_view() -> pd.DataFrame:
    classes = load_table("classes").copy()
    if classes.empty:
        return classes
    return classes.sort_values(by=["day", "time", "name", "class_id"]).reset_index(drop=True)
def get_programmes_view() -> pd.DataFrame:
    programmes = load_table("programmes").copy()
    if programmes.empty:
        return programmes
    return programmes.sort_values(by=["name", "programme_id"]).reset_index(drop=True)
def get_products_view() -> pd.DataFrame:
    products = load_table("products").copy()
    if products.empty:
        return products
    return products.sort_values(by=["name", "product_id"]).reset_index(drop=True)
def get_programme_products_view() -> pd.DataFrame:
    links = load_table("programme_products").copy()
    if links.empty:
        return links
    programmes = load_table("programmes").copy()
    products = load_table("products").copy()
    merged = links.merge(
        programmes[["programme_id", "name"]].rename(columns={"name": "programme_name"}),
        on="programme_id",
        how="left",
    ).merge(
        products[["product_id", "name"]].rename(columns={"name": "product_name"}),
        on="product_id",
        how="left",
    )
    return merged.sort_values(
        by=["programme_name", "product_name", "programme_product_id"]
    ).reset_index(drop=True)
def get_programme_classes_view() -> pd.DataFrame:
    links = load_table("programme_classes").copy()
    if links.empty:
        return links
    programmes = load_table("programmes").copy()
    classes = load_table("classes").copy()
    merged = links.merge(
        programmes[["programme_id", "name"]].rename(columns={"name": "programme_name"}),
        on="programme_id",
        how="left",
    ).merge(
        classes[["class_id", "name"]].rename(columns={"name": "class_name"}),
        on="class_id",
        how="left",
    )
    return merged.sort_values(
        by=["programme_name", "class_name", "programme_class_id"]
    ).reset_index(drop=True)
def get_enrolments_view() -> pd.DataFrame:
    enrolments = load_table("enrolments").copy()
    if enrolments.empty:
        return enrolments
    students = get_students_view()
    products = load_table("products").copy()
    merged = enrolments.merge(
        students[["student_id", "full_name"]],
        on="student_id",
        how="left",
    ).merge(
        products[["product_id", "name"]].rename(columns={"name": "product_name"}),
        on="product_id",
        how="left",
    )
    return merged.sort_values(
        by=["full_name", "product_name", "enrolment_id"]
    ).reset_index(drop=True)
def get_payment_aliases_view() -> pd.DataFrame:
    aliases = load_table("payment_aliases").copy()
    if aliases.empty:
        return aliases
    guardians = get_guardians_view()
    students = get_students_view()
    merged = aliases.merge(
        guardians[["guardian_id", "guardian_name"]],
        on="guardian_id",
        how="left",
    ).merge(
        students[["student_id", "full_name"]],
        on="student_id",
        how="left",
    )
    return merged.sort_values(
        by=["guardian_name", "alias", "alias_id"]
    ).reset_index(drop=True)
def get_bank_transactions_view() -> pd.DataFrame:
    transactions = load_table("bank_transactions").copy()
    if transactions.empty:
        return transactions
    students = get_students_view()
    guardians = get_guardians_view()
    merged = transactions.merge(
        students[["student_id", "full_name"]].rename(
            columns={"student_id": "matched_student_id", "full_name": "matched_student_name"}
        ),
        on="matched_student_id",
        how="left",
    ).merge(
        guardians[["guardian_id", "guardian_name"]].rename(
            columns={"guardian_id": "matched_guardian_id"}
        ),
        on="matched_guardian_id",
        how="left",
    )
    return merged.sort_values(
        by=["date", "transaction_id"]
    ).reset_index(drop=True)
def get_attendance_view() -> pd.DataFrame:
    attendance = load_table("attendance").copy()
    if attendance.empty:
        return attendance
    return attendance.sort_values(
        by=["session_date", "class_id", "student_id"]
    ).reset_index(drop=True)
