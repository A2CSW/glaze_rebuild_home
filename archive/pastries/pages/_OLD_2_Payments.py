import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import pandas as pd
from config import PAYMENT_TRACKER

st.title("Payments")


@st.cache_data
def load_payments(path):
    return pd.read_csv(path)


try:
    df = load_payments(PAYMENT_TRACKER)
except FileNotFoundError:
    st.error(f"Missing file: {PAYMENT_TRACKER}")
    st.stop()


st.write("Rows:", len(df))
st.dataframe(df, use_container_width=True)
