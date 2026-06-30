import pandas as pd
import streamlit as st


# -----------------------------
# CORE DATA LOADERS (CACHED)
# -----------------------------
@st.cache_data(ttl=60)
def load_students():
    return pd.read_csv("data/students.csv")


@st.cache_data(ttl=60)
def load_payments():
    return pd.read_csv("data/payments.csv")


@st.cache_data(ttl=60)
def load_register():
    return pd.read_csv("data/register.csv")


# -----------------------------
# STUDENT MASTER LOADER (CANONICAL SOURCE)
# -----------------------------
def load_students_master():
    df = pd.read_csv("data/students.csv")

    # safety checks (prevents silent schema drift)
    if "student_id" not in df.columns:
        raise ValueError("students.csv must contain 'student_id' column")

    if "name" not in df.columns:
        raise ValueError("students.csv must contain 'name' column")

    # normalisation for matching reliability
    df["student_id"] = df["student_id"].astype(str).str.strip()
    df["name"] = df["name"].astype(str).str.strip()

    return df


# -----------------------------
# SINGLE ENTRY POINT
# -----------------------------
def load_data():
    students = load_students_master()
    payments = load_payments()
    register = load_register()

    return students, payments, register
