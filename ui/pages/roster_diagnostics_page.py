from __future__ import annotations
import pandas as pd
import streamlit as st
from core.data_store import load_table
from core.exceptions import ServiceError
from services.query_service import get_classes_view
from services.roster_service import resolve_class_roster
def _safe_filter(df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
    if df.empty or column not in df.columns:
        return pd.DataFrame(columns=df.columns if not df.empty else [])
    return df[df[column].fillna("").astype(str).str.strip() == value].copy()
def render_roster_diagnostics_page() -> None:
    st.header("Roster Diagnostics")
    st.caption("Trace the class -> programme -> product -> enrolment -> roster chain.")
    classes = get_classes_view()
    if classes.empty:
        st.warning("No classes available.")
        return
    class_options = []
    class_labels: dict[str, str] = {}
    for _, row in classes.iterrows():
        class_id = str(row["class_id"]).strip()
        name = str(row.get("name", "")).strip()
        day = str(row.get("day", "")).strip()
        time = str(row.get("time", "")).strip()
        class_options.append(class_id)
        class_labels[class_id] = f"{name} | {day} {time} ({class_id})".strip()
    selected_class_id = st.selectbox(
        "Select class",
        options=class_options,
        format_func=lambda x: class_labels.get(x, x),
    )
    all_classes = load_table("classes")
    programme_classes = load_table("programme_classes")
    programme_products = load_table("programme_products")
    programmes = load_table("programmes")
    products = load_table("products")
    enrolments = load_table("enrolments")
    students = load_table("students")
    class_record = _safe_filter(all_classes, "class_id", selected_class_id)
    st.subheader("1. Class Record")
    st.dataframe(class_record, use_container_width=True, hide_index=True)
    linked_programme_rows = _safe_filter(programme_classes, "class_id", selected_class_id)
    direct_programme_id = ""
    if not class_record.empty and "programme_id" in class_record.columns:
        direct_programme_id = str(class_record.iloc[0].get("programme_id", "")).strip()
    programme_ids = set()
    if not linked_programme_rows.empty and "programme_id" in linked_programme_rows.columns:
        programme_ids.update(
            linked_programme_rows["programme_id"].fillna("").astype(str).str.strip().tolist()
        )
    if direct_programme_id:
        programme_ids.add(direct_programme_id)
    programme_ids = {x for x in programme_ids if x}
    st.subheader("2. Programme-Class Links")
    st.dataframe(linked_programme_rows, use_container_width=True, hide_index=True)
    if direct_programme_id:
        st.info(f"Direct class.programme_id: {direct_programme_id}")
    linked_programmes = programmes[
        programmes["programme_id"].fillna("").astype(str).str.strip().isin(programme_ids)
    ].copy() if programme_ids else pd.DataFrame(columns=programmes.columns)
    st.subheader("3. Resolved Programmes")
    st.dataframe(linked_programmes, use_container_width=True, hide_index=True)
    linked_product_rows = programme_products[
        programme_products["programme_id"].fillna("").astype(str).str.strip().isin(programme_ids)
    ].copy() if programme_ids else pd.DataFrame(columns=programme_products.columns)
    st.subheader("4. Programme-Product Links")
    st.dataframe(linked_product_rows, use_container_width=True, hide_index=True)
    product_ids = set()
    if not linked_product_rows.empty and "product_id" in linked_product_rows.columns:
        product_ids.update(
            linked_product_rows["product_id"].fillna("").astype(str).str.strip().tolist()
        )
    if direct_programme_id and not products.empty and "programme_id" in products.columns:
        direct_products = products[
            products["programme_id"].fillna("").astype(str).str.strip() == direct_programme_id
        ].copy()
        if not direct_products.empty and "product_id" in direct_products.columns:
            product_ids.update(
                direct_products["product_id"].fillna("").astype(str).str.strip().tolist()
            )
    product_ids = {x for x in product_ids if x}
    resolved_products = products[
        products["product_id"].fillna("").astype(str).str.strip().isin(product_ids)
    ].copy() if product_ids else pd.DataFrame(columns=products.columns)
    st.subheader("5. Resolved Products")
    st.dataframe(resolved_products, use_container_width=True, hide_index=True)
    active_enrolments = enrolments[
        enrolments["product_id"].fillna("").astype(str).str.strip().isin(product_ids)
        & (enrolments["enrolment_status"].fillna("").astype(str).str.strip() == "Active")
    ].copy() if product_ids else pd.DataFrame(columns=enrolments.columns)
    st.subheader("6. Active Enrolments")
    st.dataframe(active_enrolments, use_container_width=True, hide_index=True)
    student_ids = set()
    if not active_enrolments.empty and "student_id" in active_enrolments.columns:
        student_ids.update(
            active_enrolments["student_id"].fillna("").astype(str).str.strip().tolist()
        )
    linked_students = students[
        students["student_id"].fillna("").astype(str).str.strip().isin(student_ids)
    ].copy() if student_ids else pd.DataFrame(columns=students.columns)
    st.subheader("7. Linked Students")
    st.dataframe(linked_students, use_container_width=True, hide_index=True)
    st.subheader("8. Final Resolved Roster")
    try:
        roster = resolve_class_roster(selected_class_id)
        if roster.empty:
            st.warning("No roster resolved for this class.")
        else:
            st.success(f"Resolved {len(roster)} roster row(s).")
            st.dataframe(roster, use_container_width=True, hide_index=True)
    except ServiceError as exc:
        st.error(str(exc))
    except Exception as exc:
        st.error(f"Unexpected error: {exc}")
