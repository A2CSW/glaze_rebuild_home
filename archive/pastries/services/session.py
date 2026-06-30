import streamlit as st

def init_session():
    if "user" not in st.session_state:
        st.session_state.user = None


def login_user(user):
    st.session_state.user = user


def logout_user():
    st.session_state.user = None


def get_user():
    return st.session_state.user


def require_login():
    if not st.session_state.user:
        st.warning("Please log in to continue.")
        st.stop()


def require_role(role):
    user = st.session_state.user
    if not user or user["role"] != role:
        st.error("You do not have permission to access this page.")
        st.stop()
