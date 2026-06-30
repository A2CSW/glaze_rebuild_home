import streamlit as st
from core.normaliser import build_canonical_students

st.title("Students")

@st.cache_data
def load_students():
    return build_canonical_students(
        "/Users/stephenwoods/Documents/pastries/migration/source_registers/Register 25_26.xlsx"
    )

df = load_students()

st.write("Rows:", len(df))
st.dataframe(df, use_container_width=True)
