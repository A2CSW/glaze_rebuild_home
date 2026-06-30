from __future__ import annotations
from datetime import date
import streamlit as st
from core.exceptions import ServiceError
from services.attendance_register_service import (
    build_attendance_register,
    save_attendance_register,
)
from services.query_service import get_classes_view
def render_attendance_page() -> None:
    st.header("Attendance Register")
    classes = get_classes_view()
    if classes.empty:
        st.warning("No classes available.")
        return
    class_options = []
    class_labels: dict[str, str] = {}
    for _, row in classes.iterrows():
        class_id = str(row["class_id"]).strip()
        name = str(row["name"]).strip()
        day = str(row["day"]).strip()
        time = str(row["time"]).strip()
        label = f"{name} | {day} {time} ({class_id})".strip()
        class_options.append(class_id)
        class_labels[class_id] = label
    selected_class_id = st.selectbox(
        "Select class",
        options=class_options,
        format_func=lambda x: class_labels.get(x, x),
    )
    session_date = st.date_input(
        "Session date",
        value=date.today(),
    )
    session_date_str = str(session_date)
    try:
        register = build_attendance_register(selected_class_id, session_date_str)
    except ServiceError as exc:
        st.error(str(exc))
        return
    except Exception as exc:
        st.error(f"Unexpected error: {exc}")
        return
    if register.empty:
        st.info("No roster could be resolved for this class.")
        return
    edited = st.data_editor(
        register,
        use_container_width=True,
        hide_index=True,
        column_config={
            "student_id": st.column_config.TextColumn("Student ID", disabled=True),
            "full_name": st.column_config.TextColumn("Student Name", disabled=True),
            "status": st.column_config.SelectboxColumn(
                "Status",
                options=["Present", "Absent", "Late"],
                required=True,
            ),
            "notes": st.column_config.TextColumn("Notes"),
        },
        disabled=["student_id", "full_name"],
        key=f"attendance_editor_{selected_class_id}_{session_date_str}",
    )
    if st.button("Save Attendance Register", type="primary"):
        try:
            rows = edited.to_dict(orient="records")
            saved = save_attendance_register(
                class_id=selected_class_id,
                session_date=session_date_str,
                register_rows=rows,
            )
            st.success(f"Saved {len(saved)} attendance row(s).")
            st.rerun()
        except ServiceError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")
