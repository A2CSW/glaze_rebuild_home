import streamlit as st
from models.loader import load_data

st.title("💳 Payments")

_, payments, _ = load_data()

st.dataframe(payments, use_container_width=True)
