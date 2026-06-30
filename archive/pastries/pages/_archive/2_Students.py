import sys
import os

# 🧭 SAFE ROOT INJECTION (IDEMPOTENT)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import streamlit as st
from models.loader import load_data

st.title("👩‍🎓 Students")

students, _, _ = load_data()

st.dataframe(students, use_container_width=True)
