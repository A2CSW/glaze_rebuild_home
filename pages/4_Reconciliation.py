import streamlit as st
import pandas as pd

from models.loader import load_data
from services.reconciliation_engine import reconcile

st.title("🔄 Reconciliation Engine")

students, payments, tracker = load_data()

# -----------------------------
# BANK CSV UPLOAD (THIS WAS MISSING)
# -----------------------------
bank_file = st.file_uploader("Upload Bank CSV", type=["csv"])

if bank_file is not None:

    bank_df = pd.read_csv(bank_file)

    st.subheader("Raw Bank Data")
    st.dataframe(bank_df, use_container_width=True)

    # -----------------------------
    # RUN RECONCILIATION
    # -----------------------------
    result = reconcile(bank_df, tracker, students)

    st.subheader("Reconciliation Output")
    st.dataframe(result["reconciliation"], use_container_width=True)

    st.subheader("Unmatched Bank Transactions")
    st.dataframe(result["unmatched_bank"], use_container_width=True)

else:
    st.info("Upload a bank CSV to begin reconciliation")
