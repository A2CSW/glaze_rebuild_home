def calculate_risk(invoices_df):
    """
    Simple heuristic risk scoring per parent
    """

    risk = {}

    for _, row in invoices_df.iterrows():
        parent = row["parent_id"]

        if parent not in risk:
            risk[parent] = {"overdue": 0, "partial": 0}

        if row["status"] == "UNPAID":
            risk[parent]["overdue"] += 1
        elif row["status"] == "PARTIAL":
            risk[parent]["partial"] += 1

    scored = []

    for parent, data in risk.items():
        score = data["overdue"] * 2 + data["partial"]

        level = "LOW"
        if score > 3:
            level = "HIGH"
        elif score > 1:
            level = "MEDIUM"

        scored.append({
            "parent_id": parent,
            "risk_score": score,
            "risk_level": level
        })

    return scored
