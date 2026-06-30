from __future__ import annotations
import streamlit as st
from core.exceptions import ServiceError
from services.programme_service import create_programme, update_programme
from services.query_service import get_programmes_view
def render_programmes_page() -> None:
    st.header("Programmes")
    with st.expander("Add Programme", expanded=False):
        with st.form("add_programme_form", clear_on_submit=True):
            name = st.text_input("Programme name")
            status = st.selectbox("Status", ["Active", "Inactive", "Draft"], index=0)
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Save Programme")
        if submitted:
            try:
                record = create_programme(name=name, status=status, notes=notes)
                st.success(f"Programme created: {record['name']} ({record['programme_id']})")
                st.rerun()
            except ServiceError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
    df = get_programmes_view()
    st.write(f"Rows: {len(df)}")
    st.dataframe(df, use_container_width=True, hide_index=True)
    if df.empty:
        return
    st.subheader("Edit Existing Programme")
    programme_options = df["programme_id"].astype(str).tolist()
    labels = {
        str(row["programme_id"]): f"{row['name']} ({row['programme_id']})"
        for _, row in df.iterrows()
    }
    selected_programme_id = st.selectbox(
        "Select programme",
        options=programme_options,
        format_func=lambda x: labels.get(x, x),
    )
    row = df[df["programme_id"].astype(str) == selected_programme_id].iloc[0]
    with st.form("edit_programme_form"):
        name = st.text_input("Programme name", value=str(row.get("name", "")))
        statuses = ["Active", "Inactive", "Draft"]
        current_status = str(row.get("status", "Active"))
        status_index = statuses.index(current_status) if current_status in statuses else 0
        status = st.selectbox("Status", statuses, index=status_index)
        notes = st.text_area("Notes", value=str(row.get("notes", "")))
        submitted = st.form_submit_button("Update Programme")
    if submitted:
        try:
            record = update_programme(
                programme_id=selected_programme_id,
                name=name,
                status=status,
                notes=notes,
            )
            st.success(f"Programme updated: {record['name']} ({record['programme_id']})")
            st.rerun()
        except ServiceError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")
