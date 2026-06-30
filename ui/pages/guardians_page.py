from __future__ import annotations
import streamlit as st
from core.exceptions import ServiceError
from services.guardian_service import create_guardian, update_guardian
from services.query_service import get_guardians_view
def render_guardians_page() -> None:
    st.header("Guardians")
    with st.expander("Add Guardian", expanded=False):
        with st.form("add_guardian_form", clear_on_submit=True):
            guardian_name = st.text_input("Guardian name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Save Guardian")
        if submitted:
            try:
                record = create_guardian(
                    guardian_name=guardian_name,
                    email=email,
                    phone=phone,
                    notes=notes,
                )
                st.success(f"Guardian created: {record['guardian_name']} ({record['guardian_id']})")
                st.rerun()
            except ServiceError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
    df = get_guardians_view()
    st.write(f"Rows: {len(df)}")
    st.dataframe(df, use_container_width=True, hide_index=True)
    if df.empty:
        return
    st.subheader("Edit Existing Guardian")
    guardian_options = df["guardian_id"].astype(str).tolist()
    labels = {
        str(row["guardian_id"]): f"{row['guardian_name']} ({row['guardian_id']})"
        for _, row in df.iterrows()
    }
    selected_guardian_id = st.selectbox(
        "Select guardian",
        options=guardian_options,
        format_func=lambda x: labels.get(x, x),
    )
    row = df[df["guardian_id"].astype(str) == selected_guardian_id].iloc[0]
    with st.form("edit_guardian_form"):
        guardian_name = st.text_input("Guardian name", value=str(row.get("guardian_name", "")))
        email = st.text_input("Email", value=str(row.get("email", "")))
        phone = st.text_input("Phone", value=str(row.get("phone", "")))
        notes = st.text_area("Notes", value=str(row.get("notes", "")))
        submitted = st.form_submit_button("Update Guardian")
    if submitted:
        try:
            record = update_guardian(
                guardian_id=selected_guardian_id,
                guardian_name=guardian_name,
                email=email,
                phone=phone,
                notes=notes,
            )
            st.success(f"Guardian updated: {record['guardian_name']} ({record['guardian_id']})")
            st.rerun()
        except ServiceError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")
