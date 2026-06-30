import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import pandas as pd
from models.loader import load_data
from services.invoice_engine import load_invoices, generate_monthly_invoices
from services.payment_matching import match_payments_to_invoices
from services.family_alerts import generate_family_alerts

st.title("🏦 Finance Control Center (Level 9)")

students, payments, _ = load_data()

if st.button("Generate Monthly Invoices"):
    invoices = generate_monthly_invoices(students)
else:
    invoices = load_invoices()

invoices = match_payments_to_invoices(invoices, payments)

st.subheader("Invoices")
st.dataframe(invoices, use_container_width=True)

alerts = generate_family_alerts(invoices)

st.subheader("Alerts")

if not alerts:
    st.success("No overdue accounts 🎉")
else:
    for a in alerts:
        st.error(f"{a['parent_id']} — {a['student_id']} ({a['issue']})")
