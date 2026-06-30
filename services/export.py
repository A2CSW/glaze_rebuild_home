import pandas as pd

def export_invoices_csv(invoices):
    df = pd.DataFrame(invoices)
    path = "data/invoices_export.csv"
    df.to_csv(path, index=False)
    return path
