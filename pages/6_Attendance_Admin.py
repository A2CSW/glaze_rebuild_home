import streamlit as st
import pandas as pd

from services.session import require_login, require_role
from services.attendance import get_attendance

require_login()
require_role("admin")

st.title("📊 Attendance Review")

rows = get_attendance()

df = pd.DataFrame(
    rows,
    columns=[
        "student_id",
        "class_id",
        "date",
        "present",
        "marked_by"
    ]
)

st.dataframe(
    df,
    use_container_width=True
)

st.metric(
    "Attendance Records",
    len(df)
)
