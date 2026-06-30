import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from models.loader import load_data
from services.automation import run_daily_job

st.title("📊 Executive Dashboard (Level 10)")

students, payments, _ = load_data()

result = run_daily_job(students, payments)

kpis = result["kpis"]
alerts = result["alerts"]

st.subheader("Business KPIs")

col1, col2, col3 = st.columns(3)

col1.metric("Total Invoiced", f"£{kpis['total_invoiced']:.2f}")
col2.metric("Total Paid", f"£{kpis['total_paid']:.2f}")
col3.metric("Outstanding", f"£{kpis['outstanding']:.2f}")

st.subheader("Alerts")

if not alerts:
    st.success("No financial risks 🎉")
else:
    for a in alerts:
        st.error(f"{a['parent_id']} — {a['student_id']} ({a['issue']})")
