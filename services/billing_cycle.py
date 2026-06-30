from datetime import datetime

def current_month():
    return datetime.now().strftime("%Y-%m")


def group_payments_by_month(payments_df):
    df = payments_df.copy()
    df["month"] = df["date"].str[:7]
    return df


def monthly_paid(payments_df, student_id, month):
    df = group_payments_by_month(payments_df)
    s = df[(df["student_id"] == student_id) & (df["month"] == month)]
    return s["amount"].sum()
