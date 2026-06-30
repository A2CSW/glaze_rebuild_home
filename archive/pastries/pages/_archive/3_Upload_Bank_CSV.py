import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import hashlib

st.title("📤 Bank Upload → Payments (Level 2)")

PAYMENTS_FILE = "data/payments.csv"
UPLOAD_LOG = "data/uploads.csv"

uploaded_file = st.file_uploader("Upload bank CSV", type=["csv"])


def load_payments():
    if os.path.exists(PAYMENTS_FILE):
        return pd.read_csv(PAYMENTS_FILE)
    return pd.DataFrame(columns=["payment_id", "student_id", "amount", "date", "status"])


def save_payments(df):
    df.to_csv(PAYMENTS_FILE, index=False)


def load_uploads():
    if os.path.exists(UPLOAD_LOG):
        return pd.read_csv(UPLOAD_LOG)
    return pd.DataFrame(columns=["upload_id", "filename", "uploaded_at", "row_count"])


def save_uploads(df):
    df.to_csv(UPLOAD_LOG, index=False)


def make_upload_id(content: bytes):
    return hashlib.md5(content).hexdigest()[:10]


def next_payment_id(df):
    if df.empty:
        return "PAY001"
    last = df["payment_id"].str.replace("PAY", "").astype(int).max()
    return f"PAY{last + 1:03d}"


if uploaded_file and st.button("Process Upload"):

    file_bytes = uploaded_file.getvalue()
    upload_id = make_upload_id(file_bytes)

    uploads = load_uploads()

    if upload_id in uploads["upload_id"].values:
        st.error("This file was already uploaded.")
        st.stop()

    bank = pd.read_csv(uploaded_file)

    if not {"student_id", "amount"}.issubset(bank.columns):
        st.error("CSV must contain: student_id, amount")
        st.stop()

    payments = load_payments()

    added = 0

    for _, row in bank.iterrows():

        student_id = str(row["student_id"]).strip()
        amount = float(row["amount"])

        if amount <= 0:
            continue

        duplicate = (
            (payments["student_id"] == student_id) &
            (payments["amount"] == amount) &
            (payments["date"] == datetime.now().strftime("%Y-%m-%d"))
        ).any()

        if duplicate:
            continue

        payment_id = next_payment_id(payments)

        payments = pd.concat([payments, pd.DataFrame([{
            "payment_id": payment_id,
            "student_id": student_id,
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "paid"
        }])], ignore_index=True)

        added += 1

    save_payments(payments)

    uploads = pd.concat([uploads, pd.DataFrame([{
        "upload_id": upload_id,
        "filename": uploaded_file.name,
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "row_count": len(bank)
    }])], ignore_index=True)

    save_uploads(uploads)

    st.success(f"Imported {added} new payments")
