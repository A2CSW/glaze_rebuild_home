from services.overdue import get_overdue_invoices

def generate_family_alerts(invoices_df):
    overdue = get_overdue_invoices(invoices_df)

    alerts = []

    for _, row in overdue.iterrows():
        alerts.append({
            "parent_id": row["parent_id"],
            "student_id": row["student_id"],
            "issue": "OVERDUE INVOICE",
            "level": "HIGH"
        })

    return alerts
