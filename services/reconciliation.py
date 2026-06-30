from services.pricing_engine import calculate_student_price

def reconcile_student(student, payments_df):
    """
    Compares expected pricing vs actual payments
    """

    pricing = calculate_student_price(student)
    student_id = student["student_id"]

    actual = payments_df[payments_df["student_id"] == student_id]["amount"].sum()

    expected = pricing["total"]

    balance = actual - expected

    if balance < 0:
        status = "OWING"
    elif balance == 0:
        status = "SETTLED"
    else:
        status = "CREDIT"

    return {
        "student_id": student_id,
        "expected": expected,
        "paid": actual,
        "balance": balance,
        "status": status,
        "breakdown": pricing["breakdown"]
    }


def reconcile_all(students_df, payments_df):
    results = []

    for _, student in students_df.iterrows():
        results.append(reconcile_student(student, payments_df))

    return results
