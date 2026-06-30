from __future__ import annotations
import streamlit as st
from core.exceptions import ServiceError
from services.payment_alias_service import create_payment_alias, update_payment_alias
from services.query_service import get_guardians_view, get_payment_aliases_view, get_students_view
def render_payment_aliases_page() -> None:
    st.header("Payment Aliases")
    guardians = get_guardians_view()
    students = get_students_view()
    if guardians.empty:
        st.warning("Create at least one guardian first.")
        return
    guardian_options = []
    guardian_labels: dict[str, str] = {}
    for _, row in guardians.iterrows():
        guardian_id = str(row["guardian_id"]).strip()
        guardian_name = str(row["guardian_name"]).strip()
        guardian_options.append(guardian_id)
        guardian_labels[guardian_id] = f"{guardian_name} ({guardian_id})"
    student_options = [""]
    student_labels = {"": "(No student linked)"}
    if not students.empty:
        for _, row in students.iterrows():
            student_id = str(row["student_id"]).strip()
            full_name = str(row["full_name"]).strip()
            student_options.append(student_id)
            student_labels[student_id] = f"{full_name} ({student_id})"
    with st.expander("Add Payment Alias", expanded=False):
        with st.form("add_payment_alias_form", clear_on_submit=True):
            guardian_id = st.selectbox(
                "Guardian",
                options=guardian_options,
                format_func=lambda x: guardian_labels.get(x, x),
            )
            student_id = st.selectbox(
                "Student",
                options=student_options,
                format_func=lambda x: student_labels.get(x, x),
            )
            alias = st.text_input("Alias / Bank Reference")
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Save Alias")
        if submitted:
            try:
                record = create_payment_alias(
                    guardian_id=guardian_id,
                    student_id=student_id,
                    alias=alias,
                    notes=notes,
                )
                st.success(f"Alias created: {record['alias']} ({record['alias_id']})")
                st.rerun()
            except ServiceError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
    df = get_payment_aliases_view()
    st.write(f"Rows: {len(df)}")
    st.dataframe(df, use_container_width=True, hide_index=True)
    if df.empty:
        return
    st.subheader("Edit Existing Alias")
    alias_options = df["alias_id"].astype(str).tolist()
    labels = {
        str(row["alias_id"]): f"{row['alias']} ({row['alias_id']})"
        for _, row in df.iterrows()
    }
    selected_alias_id = st.selectbox(
        "Select alias",
        options=alias_options,
        format_func=lambda x: labels.get(x, x),
    )
    row = df[df["alias_id"].astype(str) == selected_alias_id].iloc[0]
    current_guardian_id = str(row.get("guardian_id", ""))
    current_student_id = str(row.get("student_id", ""))
    guardian_index = guardian_options.index(current_guardian_id) if current_guardian_id in guardian_options else 0
    student_index = student_options.index(current_student_id) if current_student_id in student_options else 0
    with st.form("edit_payment_alias_form"):
        guardian_id = st.selectbox(
            "Guardian",
            options=guardian_options,
            index=guardian_index,
            format_func=lambda x: guardian_labels.get(x, x),
        )
        student_id = st.selectbox(
            "Student",
            options=student_options,
            index=student_index,
            format_func=lambda x: student_labels.get(x, x),
        )
        alias = st.text_input("Alias / Bank Reference", value=str(row.get("alias", "")))
        notes = st.text_area("Notes", value=str(row.get("notes", "")))
        submitted = st.form_submit_button("Update Alias")
    if submitted:
        try:
            record = update_payment_alias(
                alias_id=selected_alias_id,
                guardian_id=guardian_id,
                student_id=student_id,
                alias=alias,
                notes=notes,
            )
            st.success(f"Alias updated: {record['alias']} ({record['alias_id']})")
            st.rerun()
        except ServiceError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")
