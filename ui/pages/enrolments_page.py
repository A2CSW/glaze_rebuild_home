from __future__ import annotations
import streamlit as st
from core.exceptions import ServiceError
from services.enrolment_service import create_enrolment, update_enrolment
from services.query_service import get_enrolments_view, get_products_view, get_students_view
def render_enrolments_page() -> None:
    st.header("Enrolments")
    students = get_students_view()
    products = get_products_view()
    if students.empty:
        st.warning("Create at least one student first.")
        return
    if products.empty:
        st.warning("Create at least one product first.")
        return
    student_options = []
    student_labels: dict[str, str] = {}
    for _, row in students.iterrows():
        student_id = str(row["student_id"]).strip()
        full_name = str(row["full_name"]).strip()
        student_options.append(student_id)
        student_labels[student_id] = f"{full_name} ({student_id})"
    product_options = []
    product_labels: dict[str, str] = {}
    for _, row in products.iterrows():
        product_id = str(row["product_id"]).strip()
        product_name = str(row["name"]).strip()
        product_options.append(product_id)
        product_labels[product_id] = f"{product_name} ({product_id})"
    with st.expander("Add Enrolment", expanded=False):
        with st.form("add_enrolment_form", clear_on_submit=True):
            student_id = st.selectbox(
                "Student",
                options=student_options,
                format_func=lambda x: student_labels.get(x, x),
            )
            product_id = st.selectbox(
                "Product",
                options=product_options,
                format_func=lambda x: product_labels.get(x, x),
            )
            start_date = st.text_input("Start date (YYYY-MM-DD)")
            end_date = st.text_input("End date (optional)")
            enrolment_status = st.selectbox(
                "Status",
                ["Active", "Inactive", "Cancelled", "Completed", "Pending"],
                index=0,
            )
            submitted = st.form_submit_button("Save Enrolment")
        if submitted:
            try:
                record = create_enrolment(
                    student_id=student_id,
                    product_id=product_id,
                    start_date=start_date,
                    end_date=end_date,
                    enrolment_status=enrolment_status,
                )
                st.success(f"Enrolment created: {record['enrolment_id']}")
                st.rerun()
            except ServiceError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
    df = get_enrolments_view()
    st.write(f"Rows: {len(df)}")
    st.dataframe(df, use_container_width=True, hide_index=True)
    if df.empty:
        return
    st.subheader("Edit Existing Enrolment")
    enrolment_options = df["enrolment_id"].astype(str).tolist()
    labels = {
        str(row["enrolment_id"]): f"{row['full_name']} -> {row['product_name']} ({row['enrolment_id']})"
        for _, row in df.iterrows()
    }
    selected_enrolment_id = st.selectbox(
        "Select enrolment",
        options=enrolment_options,
        format_func=lambda x: labels.get(x, x),
    )
    row = df[df["enrolment_id"].astype(str) == selected_enrolment_id].iloc[0]
    current_student_id = str(row.get("student_id", ""))
    current_product_id = str(row.get("product_id", ""))
    student_index = student_options.index(current_student_id) if current_student_id in student_options else 0
    product_index = product_options.index(current_product_id) if current_product_id in product_options else 0
    with st.form("edit_enrolment_form"):
        student_id = st.selectbox(
            "Student",
            options=student_options,
            index=student_index,
            format_func=lambda x: student_labels.get(x, x),
        )
        product_id = st.selectbox(
            "Product",
            options=product_options,
            index=product_index,
            format_func=lambda x: product_labels.get(x, x),
        )
        start_date = st.text_input("Start date (YYYY-MM-DD)", value=str(row.get("start_date", "")))
        end_date = st.text_input("End date (optional)", value=str(row.get("end_date", "")))
        statuses = ["Active", "Inactive", "Cancelled", "Completed", "Pending"]
        current_status = str(row.get("enrolment_status", "Active"))
        status_index = statuses.index(current_status) if current_status in statuses else 0
        enrolment_status = st.selectbox("Status", statuses, index=status_index)
        submitted = st.form_submit_button("Update Enrolment")
    if submitted:
        try:
            record = update_enrolment(
                enrolment_id=selected_enrolment_id,
                student_id=student_id,
                product_id=product_id,
                start_date=start_date,
                end_date=end_date,
                enrolment_status=enrolment_status,
            )
            st.success(f"Enrolment updated: {record['enrolment_id']}")
            st.rerun()
        except ServiceError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")
