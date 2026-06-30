import streamlit as st
from models.loader import load_data

st.title("👩‍🎓 Students")

students, _, _ = load_data()

st.dataframe(students, use_container_width=True)
