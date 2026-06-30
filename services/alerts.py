def generate_alerts(students, payments, register):
    alerts = []

    for _, student in students.iterrows():
        sid = student["student_id"]

        total_paid = payments[payments["student_id"] == sid]["amount"].sum()
        attendance = register[register["student_id"] == sid]["present"].mean()

        if total_paid < 20:
            alerts.append((sid, "PAYMENT RISK", "HIGH"))

        if attendance < 0.5:
            alerts.append((sid, "ATTENDANCE RISK", "MEDIUM"))

    return alerts
