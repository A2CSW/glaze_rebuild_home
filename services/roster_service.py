from __future__ import annotations
import pandas as pd
from core.data_store import load_table
from core.exceptions import ServiceError
ACTIVE_ENROLMENT_STATUSES = {"Active"}
def resolve_class_roster(class_id: str) -> pd.DataFrame:
    class_id = class_id.strip()
    if not class_id:
        raise ServiceError("class_id is required.")
    classes = load_table("classes")
    programme_classes = load_table("programme_classes")
    programme_products = load_table("programme_products")
    enrolments = load_table("enrolments")
    students = load_table("students")
    class_match = classes[
        classes["class_id"].astype(str).str.strip() == class_id
    ].copy()
    if class_match.empty:
        raise ServiceError(f"Class not found: {class_id}")
    programme_ids: set[str] = set()
    linked_programmes = programme_classes[
        programme_classes["class_id"].astype(str).str.strip() == class_id
    ].copy()
    if not linked_programmes.empty:
        programme_ids.update(
            linked_programmes["programme_id"].fillna("").astype(str).str.strip()
        )
    direct_programme_id = str(class_match.iloc[0].get("programme_id", "")).strip()
    if direct_programme_id:
        programme_ids.add(direct_programme_id)
    programme_ids = {pid for pid in programme_ids if pid}
    if not programme_ids:
        return pd.DataFrame(columns=["student_id", "full_name", "status"])
    linked_products = programme_products[
        programme_products["programme_id"]
        .fillna("")
        .astype(str)
        .str.strip()
        .isin(programme_ids)
    ].copy()
    if linked_products.empty:
        return pd.DataFrame(columns=["student_id", "full_name", "status"])
    product_ids = set(
        linked_products["product_id"].fillna("").astype(str).str.strip()
    )
    active_enrolments = enrolments[
        enrolments["product_id"].fillna("").astype(str).str.strip().isin(product_ids)
        & enrolments["enrolment_status"]
        .fillna("")
        .astype(str)
        .str.strip()
        .isin(ACTIVE_ENROLMENT_STATUSES)
    ].copy()
    if active_enrolments.empty:
        return pd.DataFrame(columns=["student_id", "full_name", "status"])
    student_ids = set(
        active_enrolments["student_id"].fillna("").astype(str).str.strip()
    )
    roster = students[
        students["student_id"].fillna("").astype(str).str.strip().isin(student_ids)
    ].copy()
    if roster.empty:
        return pd.DataFrame(columns=["student_id", "full_name", "status"])
    if "full_name" not in roster.columns:
        roster["full_name"] = (
            roster["first_name"].fillna("").astype(str).str.strip()
            + " "
            + roster["last_name"].fillna("").astype(str).str.strip()
        ).str.strip()
    roster = roster[["student_id", "full_name", "status"]].drop_duplicates()
    roster = roster.sort_values(by=["full_name", "student_id"]).reset_index(drop=True)
    return roster
