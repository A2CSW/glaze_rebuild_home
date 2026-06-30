import sys
from pathlib import Path

# =============================================
# PROJECT ROOT PATH
# =============================================

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)


import streamlit as st
import pandas as pd
import os

from services.reconciliation_engine import build_payment_queue
from core.data_loader import load_all

st.title("📤 Bank Upload → Payment Review")


PAYMENTS_FILE = "data/payments.csv"


# =============================================
# LOAD PAYMENTS
# =============================================

def load_payments():

    if os.path.exists(PAYMENTS_FILE):
        return pd.read_csv(PAYMENTS_FILE)

    return pd.DataFrame(
        columns=[
            "payment_id",
            "student_id",
            "amount",
            "date",
            "status"
        ]
    )


def save_payments(df):

    df.to_csv(
        PAYMENTS_FILE,
        index=False
    )


# =============================================
# UPLOAD
# =============================================

uploaded_file = st.file_uploader(
    "Upload bank CSV",
    type=["csv"]
)


if uploaded_file:


    bank = pd.read_csv(uploaded_file)


    st.success(
        f"Loaded {len(bank)} transactions"
    )

    # -----------------------------------------
    # LOAD STUDENTS
    # -----------------------------------------

    students, attendance, payments, medical, contacts, memberships, addons, enrolments = load_all()


    # -----------------------------------------
    # CLEAN + MATCH
    # -----------------------------------------

    queue = build_payment_queue(
        bank,
        students
    )


    # =============================================
    # PAYMENT REVIEW QUEUE
    # =============================================

    st.divider()

    st.subheader(
        "Payment Review Queue"
    )


    display = queue[
        [
            "description",
            "amount",
            "matched_name",
            "confidence",
            "matched_student_id"
        ]
    ].copy()


    display["Approve"] = (
        display["confidence"] >= 80
    )


    edited = st.data_editor(
        display,
        use_container_width=True,
        hide_index=True,
        disabled=[
            "description",
            "amount",
            "matched_name",
            "confidence",
            "matched_student_id"
        ]
    )


    approved = edited[
        edited["Approve"]
    ]


    st.info(
        f"{len(approved)} payments ready to import"
    )

    # =============================================
    # SAVE APPROVED PAYMENTS
    # =============================================

    if st.button(
        "✅ Import Approved Payments",
        type="primary"
    ):


        payments = load_payments()


        added = 0


        for _, row in approved.iterrows():


            if pd.isna(
                row["matched_student_id"]
            ):
                continue


            payments.loc[len(payments)] = {

                "payment_id":
                    f"PAY{len(payments)+1:04d}",

                "student_id":
                    row["matched_student_id"],

                "amount":
                    row["amount"],

                "date":
                    pd.Timestamp.now()
                    .strftime("%Y-%m-%d"),

                "status":
                    "approved"
            }


            added += 1


        save_payments(payments)


        st.success(
            f"Imported {added} payments"
        )
