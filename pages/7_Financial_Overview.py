import streamlit as st
import pandas as pd
from models.loader import load_data
from services.reconciliation import reconcile_all

st.title("💰 Level 6: Live Reconciliation Engine")

students, payments, _ = load_data()

results = reconcile_all(students, payments)

df = pd.DataFrame(results)

st.dataframe(df, use_container_width=True)

st.subheader("Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Owing", len(df[df["status"] == "OWING"]))
col2.metric("Settled", len(df[df["status"] == "SETTLED"]))
col3.metric("Credit", len(df[df["status"] == "CREDIT"]))

st.subheader("Total Financial Position")

st.metric("Net Balance",
          f"£{df['balance'].sum():.2f}")
