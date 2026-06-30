import streamlit as st
import pandas as pd
from models.loader import load_data
from services.invoices import generate_all_invoices
from services.export import export_invoices_csv

st.title("🧾 Monthly Invoices (Level 7)")

students, payments, _ = load_data()

invoices = generate_all_invoices(students, payments)

df = pd.DataFrame(invoices)

st.dataframe(df, use_container_width=True)

if st.button("Export CSV"):
    path = export_invoices_csv(invoices)
    st.success(f"Exported to {path}")

st.subheader("Summary")

st.metric("Owing", len(df[df["status"] == "OWING"]))
st.metric("OK", len(df[df["status"] == "OK"]))
