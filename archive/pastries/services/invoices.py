from services.pricing_engine import calculate_student_price
from services.billing_cycle import current_month, monthly_paid

def generate_invoice(student, payments_df, month=None):
    if month is None:
        month = current_month()

    pricing = calculate_student_price(student)
    expected_monthly = pricing["total"] / 12  # simplified monthly spread

    paid = monthly_paid(payments_df, student["student_id"], month)

    balance = paid - expected_monthly

    status = "OWING" if balance < 0 else "OK"

    return {
        "student_id": student["student_id"],
        "month": month,
        "expected": expected_monthly,
        "paid": paid,
        "balance": balance,
        "status": status
    }


def generate_all_invoices(students_df, payments_df, month=None):
    results = []

    for _, student in students_df.iterrows():
        results.append(generate_invoice(student, payments_df, month))

    return results
