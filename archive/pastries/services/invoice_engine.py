import pandas as pd
from datetime import datetime
from services.pricing_engine import calculate_student_price

INVOICE_FILE = "data/invoices.csv"


def load_invoices():
    try:
        return pd.read_csv(INVOICE_FILE)
    except:
        return pd.DataFrame(columns=[
            "invoice_id","parent_id","student_id","month","amount","status","created_at"
        ])


def save_invoices(df):
    df.to_csv(INVOICE_FILE, index=False)


def generate_invoice_id(df):
    if df.empty:
        return "INV001"
    last = df["invoice_id"].str.replace("INV", "").astype(int).max()
    return f"INV{last + 1:03d}"


def generate_monthly_invoices(students_df, month="2026-06"):
    invoices = load_invoices()

    new_rows = []

    for _, student in students_df.iterrows():

        pricing = calculate_student_price(student)
        amount = pricing["total"] / 12  # monthly spread

        invoice_id = generate_invoice_id(invoices)

        new_rows.append({
            "invoice_id": invoice_id,
            "parent_id": student.get("parent_id", "UNKNOWN"),
            "student_id": student["student_id"],
            "month": month,
            "amount": amount,
            "status": "UNPAID",
            "created_at": datetime.now().strftime("%Y-%m-%d")
        })

    invoices = pd.concat([invoices, pd.DataFrame(new_rows)], ignore_index=True)
    save_invoices(invoices)

    return invoices
