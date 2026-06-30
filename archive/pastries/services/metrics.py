import pandas as pd

def calculate_kpis(invoices_df, payments_df):
    total_invoiced = invoices_df["amount"].sum()
    total_paid = payments_df["amount"].sum()

    outstanding = total_invoiced - total_paid

    paid_invoices = invoices_df[invoices_df["status"] == "PAID"]
    unpaid_invoices = invoices_df[invoices_df["status"] == "UNPAID"]

    return {
        "total_invoiced": total_invoiced,
        "total_paid": total_paid,
        "outstanding": outstanding,
        "paid_invoices": len(paid_invoices),
        "unpaid_invoices": len(unpaid_invoices)
    }
