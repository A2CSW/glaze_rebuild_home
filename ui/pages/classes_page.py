from __future__ import annotations
import streamlit as st
from core.exceptions import ServiceError
from services.class_service import create_class, update_class
from services.query_service import get_classes_view, get_programmes_view
def render_classes_page() -> None:
    st.header("Classes")
    programmes = get_programmes_view()
    programme_options = [""]
    programme_labels = {"": "(No programme linked)"}
    if not programmes.empty:
        for _, row in programmes.iterrows():
            programme_id = str(row["programme_id"]).strip()
            programme_name = str(row["name"]).strip()
            programme_options.append(programme_id)
            programme_labels[programme_id] = f"{programme_name} ({programme_id})"
    with st.expander("Add Class", expanded=False):
        with st.form("add_class_form", clear_on_submit=True):
            name = st.text_input("Class name")
            programme_id = st.selectbox(
                "Programme",
                options=programme_options,
                format_func=lambda x: programme_labels.get(x, x),
            )
            calendar_id = st.text_input("Calendar ID")
            day = st.selectbox(
                "Day",
                ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                index=0,
            )
            time = st.text_input("Time (e.g. 16:00)")
            status = st.selectbox("Status", ["Active", "Inactive"], index=0)
            submitted = st.form_submit_button("Save Class")
        if submitted:
            try:
                record = create_class(
                    name=name,
                    programme_id=programme_id,
                    calendar_id=calendar_id,
                    day=day,
                    time=time,
                    status=status,
                )
                st.success(f"Class created: {record['name']} ({record['class_id']})")
                st.rerun()
            except ServiceError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
    df = get_classes_view()
    st.write(f"Rows: {len(df)}")
    st.dataframe(df, use_container_width=True, hide_index=True)
    if df.empty:
        return
    st.subheader("Edit Existing Class")
    class_options = df["class_id"].astype(str).tolist()
    labels = {
        str(row["class_id"]): f"{row['name']} ({row['class_id']})"
        for _, row in df.iterrows()
    }
    selected_class_id = st.selectbox(
        "Select class",
        options=class_options,
        format_func=lambda x: labels.get(x, x),
    )
    row = df[df["class_id"].astype(str) == selected_class_id].iloc[0]
    current_programme_id = str(row.get("programme_id", ""))
    programme_index = programme_options.index(current_programme_id) if current_programme_id in programme_options else 0
    with st.form("edit_class_form"):
        name = st.text_input("Class name", value=str(row.get("name", "")))
        programme_id = st.selectbox(
            "Programme",
            options=programme_options,
            index=programme_index,
            format_func=lambda x: programme_labels.get(x, x),
        )
        calendar_id = st.text_input("Calendar ID", value=str(row.get("calendar_id", "")))
        days = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        current_day = str(row.get("day", ""))
        day_index = days.index(current_day) if current_day in days else 0
        day = st.selectbox("Day", days, index=day_index)
        time = st.text_input("Time (e.g. 16:00)", value=str(row.get("time", "")))
        statuses = ["Active", "Inactive"]
        current_status = str(row.get("status", "Active"))
        status_index = statuses.index(current_status) if current_status in statuses else 0
        status = st.selectbox("Status", statuses, index=status_index)
        submitted = st.form_submit_button("Update Class")
    if submitted:
        try:
            record = update_class(
                class_id=selected_class_id,
                name=name,
                programme_id=programme_id,
                calendar_id=calendar_id,
                day=day,
                time=time,
                status=status,
            )
            st.success(f"Class updated: {record['name']} ({record['class_id']})")
            st.rerun()
        except ServiceError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")
