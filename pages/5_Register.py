import streamlit as st
from datetime import date
from services.session import require_login, get_user
from services.attendance import save_attendance
import pandas as pd

require_login()

st.title("📝 Take Register")

students = pd.read_csv("data/students.csv")

user = get_user()

register_date = st.date_input(
    "Register Date",
    value=date.today()
)

class_id = st.text_input(
    "Class",
    value="Drama"
)

attendance = {}

for _, student in students.iterrows():
    attendance[student["student_id"]] = st.checkbox(
        f"{student['name']} ({student['student_id']})",
        value=True
    )

if st.button("Save Register"):

    saved = 0
    skipped = 0

    for student_id, present in attendance.items():

        success = save_attendance(
            student_id=student_id,
            class_id=class_id,
            date=str(register_date),
            present=present,
            marked_by=user["username"]
        )

        if success:
            saved += 1
        else:
            skipped += 1

    st.success(
        f"Saved: {saved} | Already existed: {skipped}"
    )
