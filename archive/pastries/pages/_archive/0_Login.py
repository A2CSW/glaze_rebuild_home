import sys
import os

# 🧭 SAFE ROOT INJECTION (IDEMPOTENT)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import streamlit as st
from services.auth import authenticate
from services.session import login_user, init_session, get_user

init_session()

st.title("🔐 Login")

user = get_user()

if user:
    st.success(f"Logged in as {user['username']}")

    if st.button("Logout"):
        from services.session import logout_user
        logout_user()
        st.rerun()

    st.stop()

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user = authenticate(username, password)

    if user:
        login_user(user)
        st.success("Login successful")
        st.rerun()
    else:
        st.error("Invalid credentials")
