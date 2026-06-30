from __future__ import annotations
import streamlit as st
from core.exceptions import ServiceError
from services.query_service import get_students_view
from services.student_service import create_student, update_student


def render_students_page() -> None:
    st.header("Students")
    st.caption("Manage students and their guardians")

    # ====================== ADD STUDENT ======================
    with st.expander("➕ Add New Student", expanded=False):
        with st.form("add_student_form", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                first_name = st.text_input("First Name *", placeholder="John")
                last_name = st.text_input("Last Name *", placeholder="Smith")
                status = st.selectbox(
                    "Status",
                    ["Current", "Former", "Taster", "Inactive"],
                    index=0,
                )

            with col2:
                guardian_first = st.text_input("Guardian First Name")
                guardian_last = st.text_input("Guardian Last Name")
                telephone = st.text_input("Telephone")
                email = st.text_input("Email")

            notes = st.text_area("Notes", height=100)

            submitted = st.form_submit_button("Save Student", use_container_width=True)

        if submitted:
            try:
                # Note: service will need updating for new guardian fields
                record = create_student(
                    first_name=first_name,
                    last_name=last_name,
                    status=status,
                    guardian_id="",          # temporary
                    date_of_birth="",        # removed field
                    search_rule="",          # removed field
                    notes=notes,
                )
                st.success(f"✅ Student created: **{record.get('full_name', 'New Student')}**")
                st.rerun()
            except ServiceError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")

    # ====================== VIEW ======================
    df = get_students_view()
    st.write(f"Rows: {len(df)}")
    st.dataframe(df, use_container_width=True, hide_index=True)

    if df.empty:
        return

    # ====================== EDIT (unchanged for now) ======================
    st.subheader("Edit Existing Student")
    student_options = df["student_id"].astype(str).tolist()
    labels = {
        str(row["student_id"]): f"{row['full_name']} ({row['student_id']})"
        for _, row in df.iterrows()
    }
    selected_student_id = st.selectbox(
        "Select student",
        options=student_options,
        format_func=lambda x: labels.get(x, x),
    )
    row = df[df["student_id"].astype(str) == selected_student_id].iloc[0]

    with st.form("edit_student_form"):
        first_name = st.text_input("First name", value=str(row.get("first_name", "")))
        last_name = st.text_input("Last name", value=str(row.get("last_name", "")))
        status = st.selectbox(
            "Status",
            ["Current", "Former", "Taster", "Inactive"],
            index=["Current", "Former", "Taster", "Inactive"].index(str(row.get("status", "Current"))),
        )
        guardian_id = st.text_input("Guardian ID", value=str(row.get("guardian_id", "")))
        notes = st.text_area("Notes", value=str(row.get("notes", "")))

        submitted = st.form_submit_button("Update Student")

    if submitted:
        try:
            record = update_student(
                student_id=selected_student_id,
                first_name=first_name,
                last_name=last_name,
                status=status,
                guardian_id=guardian_id,
                date_of_birth="", 
                search_rule="",
                notes=notes,
            )
            st.success(f"Student updated: {record.get('full_name')} ({record['student_id']})")
            st.rerun()
        except ServiceError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")
