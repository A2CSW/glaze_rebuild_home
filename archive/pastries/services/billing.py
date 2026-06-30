from services.pricing import PRICING

def calculate_student_plan(student, payments_df):
    """
    Minimal viable billing model:
    - core membership
    - ignores optional add-ons for now (we expand later)
    """

    status = student.get("status", "active")

    # Default assumption (you will refine later per student attributes)
    expected_monthly = PRICING["core_class"]

    student_payments = payments_df[payments_df["student_id"] == student["student_id"]]
    total_paid = student_payments["amount"].sum()

    expected_annual = expected_monthly * 12
    balance = total_paid - expected_annual

    if balance < 0:
        state = "OWING"
    elif balance == 0:
        state = "OK"
    else:
        state = "CREDIT"

    return {
        "student_id": student["student_id"],
        "expected_monthly": expected_monthly,
        "expected_annual": expected_annual,
        "paid": total_paid,
        "balance": balance,
        "state": state
    }
