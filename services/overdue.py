def get_overdue_invoices(invoices_df):
    return invoices_df[invoices_df["status"] == "UNPAID"]
