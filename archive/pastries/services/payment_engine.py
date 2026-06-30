import pandas as pd

EXPECTED_FEE = 44


# -----------------------------
# CORE: NORMALISE BANK DATA
# -----------------------------
def normalize_bank_csv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Expected columns (flexible input):
    - student_id OR reference OR name
    - amount
    - date
    """

    df = df.copy()

    # standardise column names if needed
    df.columns = [c.strip().lower() for c in df.columns]

    # ensure required fields exist
    if "amount" not in df.columns:
        raise ValueError("Bank CSV must include 'amount' column")

    if "student_id" not in df.columns:
        df["student_id"] = None

    return df[["student_id", "amount", "date"] if "date" in df.columns else ["student_id", "amount"]]


# -----------------------------
# CORE: LEDGER BUILD
# -----------------------------
def build_ledger(payments_df: pd.DataFrame) -> pd.DataFrame:
    df = payments_df.copy()

    if "student_id" not in df.columns:
        raise ValueError("Payments table must include student_id")

    return (
        df.groupby("student_id", as_index=False)
          .agg(total_paid=("amount", "sum"))
    )


# -----------------------------
# CORE: STATUS ENGINE
# -----------------------------
def compute_status(ledger: pd.DataFrame, expected_fee: float = EXPECTED_FEE) -> pd.DataFrame:
    df = ledger.copy()

    def status(row):
        if row["total_paid"] >= expected_fee:
            return "PAID"
        elif row["total_paid"] > 0:
            return "PARTIAL"
        return "UNPAID"

    df["status"] = df.apply(status, axis=1)
    df["expected"] = expected_fee
    df["balance"] = df["expected"] - df["total_paid"]

    return df


# -----------------------------
# PIPELINE: END-TO-END
# -----------------------------
def run_payment_pipeline(payments_df: pd.DataFrame) -> pd.DataFrame:
    ledger = build_ledger(payments_df)
    return compute_status(ledger)
