import sys
import os

# 🧭 SAFE ROOT INJECTION (IDEMPOTENT)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import streamlit as st
from models.loader import load_data
from services.family_billing import build_family_accounts

st.title("👨‍👩‍👧 Family Accounts (Level 8)")

students, payments, _ = load_data()

families = build_family_accounts(students, payments)

for family in families:

    st.subheader(f"Parent: {family['parent_id']}")

    col1, col2, col3 = st.columns(3)

    col1.metric("Expected", f"£{family['total_expected']:.2f}")
    col2.metric("Paid", f"£{family['total_paid']:.2f}")
    col3.metric("Balance", f"£{family['total_balance']:.2f}")

    st.markdown("### Children")

    for child in family["children"]:
        st.write(
            f"{child['student_id']} — "
            f"£{child['expected']:.2f} expected | "
            f"£{child['paid']:.2f} paid | "
            f"{child['status']}"
        )

    st.divider()
