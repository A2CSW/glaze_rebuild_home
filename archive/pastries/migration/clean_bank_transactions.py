import pandas as pd

IN_FILE = "migration/output/transactions_raw.csv"
OUT_FILE = "migration/output/transactions_clean.csv"


def clean(df):
    df = df.copy()

    # 1. standardise column names
    df.columns = [c.lower().strip() for c in df.columns]

    print("COLUMNS FOUND:", df.columns.tolist())

    # 2. drop fully empty rows
    df = df.dropna(how="all")

    return df


def normalise_amounts(df):
    df = df.copy()

    debit_col = None
    credit_col = None

    for c in df.columns:
        if "debit" in c:
            debit_col = c
        if "credit" in c:
            credit_col = c

    if debit_col is None and credit_col is None:
        raise ValueError(f"No debit/credit columns found in: {df.columns.tolist()}")

    df["amount_signed"] = 0

    if debit_col:
        df[debit_col] = pd.to_numeric(df[debit_col], errors="coerce").fillna(0)
        df["amount_signed"] -= df[debit_col]

    if credit_col:
        df[credit_col] = pd.to_numeric(df[credit_col], errors="coerce").fillna(0)
        df["amount_signed"] += df[credit_col]

    return df


def main():
    df = pd.read_csv(IN_FILE)

    df_clean = clean(df)
    df_clean = normalise_amounts(df_clean)

    print("CLEAN ROWS:", len(df_clean))
    print(df_clean.head(20))

    df_clean.to_csv(OUT_FILE, index=False)
    print("Saved →", OUT_FILE)


if __name__ == "__main__":
    main()
