import pandas as pd

def forecast_cashflow(invoices_df):
    """
    Simple forward projection:
    assumes unpaid invoices are collected over next 30 days
    """

    unpaid = invoices_df[invoices_df["status"] == "UNPAID"]["amount"].sum()
    partial = invoices_df[invoices_df["status"] == "PARTIAL"]["amount"].sum()

    return {
        "expected_next_30_days": unpaid + (partial * 0.5),
        "risk_exposure": unpaid
    }
