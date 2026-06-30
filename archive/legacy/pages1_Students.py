import streamlit as st
from core.normaliser import build_canonical_students

st.title("Students")

df = build_canonical_students(
    "/Users/stephenwoods/Documents/pastries/migration/source_registers/Register 25_26.xlsx"
)

st.write("Rows:", len(df))
st.write("Columns:", df.columns.tolist())

st.dataframe(df, use_container_width=True)
