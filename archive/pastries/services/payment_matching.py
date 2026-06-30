import pandas as pd

def match_payments_to_invoices(invoices_df, payments_df):
    """
    Marks invoices as PAID if payments exist
    """

    invoices = invoices_df.copy()

    for i, inv in invoices.iterrows():

        paid = payments_df[
            (payments_df["student_id"] == inv["student_id"]) &
            (payments_df["amount"] >= inv["amount"])
        ]["amount"].sum()

        if paid >= inv["amount"]:
            invoices.at[i, "status"] = "PAID"
        elif paid > 0:
            invoices.at[i, "status"] = "PARTIAL"
        else:
            invoices.at[i, "status"] = "UNPAID"

    return invoices
