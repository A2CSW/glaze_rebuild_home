import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from core.normaliser import build_canonical_students

st.title("Students")

df = build_canonical_students(
    "/Users/stephenwoods/Documents/pastries/migration/source_registers/Register 25_26.xlsx"
)

st.write("Total students:", len(df))
st.dataframe(df, use_container_width=True)
