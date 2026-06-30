import pandas as pd
from core.schema import REQUIRED_STUDENT_COLUMNS, REQUIRED_PAYMENT_COLUMNS

def clean_students(df):
    df = df.copy()

    for col in REQUIRED_STUDENT_COLUMNS:
        if col not in df.columns:
            df[col] = None

    df["student_id"] = df["student_id"].astype(str)

    return df


def clean_payments(df):
    df = df.copy()

    for col in REQUIRED_PAYMENT_COLUMNS:
        if col not in df.columns:
            df[col] = None

    df["student_id"] = df["student_id"].astype(str)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    return df

