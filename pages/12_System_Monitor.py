import streamlit as st
from models.loader import load_data
from services.scheduler import run_daily_system
from services.audit import get_logs

st.title("🛠 System Monitor (Level 11)")

students, payments, _ = load_data()

result = run_daily_system(students, payments)

st.subheader("System KPIs")
st.json(result["kpis"])

st.subheader("Recent Audit Logs")

logs = get_logs()

for log in logs[:20]:
    st.write(log)
