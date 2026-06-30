import streamlit as st
from models.loader import load_data
from services.payment_engine import run_payment_pipeline

st.title("📊 Dashboard")

students, payments, register = load_data()

st.metric("Students", len(students))

summary = run_payment_pipeline(payments)

paid = len(summary[summary["status"] == "PAID"])

st.metric("Paid Students", paid)

st.subheader("Payment Overview")
st.dataframe(summary, use_container_width=True)
