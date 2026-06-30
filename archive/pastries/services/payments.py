import pandas as pd

EXPECTED_FEE = 44

def payment_status(payments_df, student_id):
    student_payments = payments_df[payments_df["student_id"] == student_id]
    total = student_payments["amount"].sum()

    if total >= EXPECTED_FEE:
        return "PAID"
    elif total > 0:
        return "PARTIAL"
    else:
        return "NO PAYMENT"


def student_payment_summary(students_df, payments_df):
    results = []

    for _, student in students_df.iterrows():
        sid = student["student_id"]
        status = payment_status(payments_df, sid)

        total_paid = payments_df[payments_df["student_id"] == sid]["amount"].sum()

        results.append({
            "student_id": sid,
            "name": student["name"],
            "total_paid": total_paid,
            "expected": EXPECTED_FEE,
            "status": status
        })

    return pd.DataFrame(results)


def overdue_students(summary_df):
    return summary_df[summary_df["status"] != "PAID"]
