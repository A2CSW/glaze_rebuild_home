import sys
import os

# 🧭 SAFE ROOT INJECTION (IDEMPOTENT)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import streamlit as st
from models.loader import load_data
from services.alerts import generate_alerts

st.title("🚨 Alerts")

students, payments, register = load_data()

alerts = generate_alerts(students, payments, register)

if not alerts:
    st.success("No alerts 🎉")
else:
    for sid, issue, level in alerts:
        if level == "HIGH":
            st.error(f"{sid} — {issue}")
        else:
            st.warning(f"{sid} — {issue}")
