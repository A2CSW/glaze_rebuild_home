from services.reconciliation import reconcile_all

def build_family_accounts(students_df, payments_df):
    """
    Groups all financials by parent_id
    """

    reconciled = reconcile_all(students_df, payments_df)

    families = {}

    for student in reconciled:
        sid = student["student_id"]

        # find parent_id
        parent_id = None
        for _, row in students_df.iterrows():
            if row["student_id"] == sid:
                parent_id = row.get("parent_id", "UNKNOWN")
                name = row.get("name", sid)
                break

        if parent_id not in families:
            families[parent_id] = {
                "parent_id": parent_id,
                "children": [],
                "total_expected": 0,
                "total_paid": 0,
                "total_balance": 0
            }

        families[parent_id]["children"].append({
            "student_id": sid,
            "expected": student["expected"],
            "paid": student["paid"],
            "balance": student["balance"],
            "status": student["status"]
        })

        families[parent_id]["total_expected"] += student["expected"]
        families[parent_id]["total_paid"] += student["paid"]
        families[parent_id]["total_balance"] += student["balance"]

    return list(families.values())
