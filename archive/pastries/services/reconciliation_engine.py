import pandas as pd
from rapidfuzz import fuzz
import re

# -----------------------------
# FUZZY MATCH ENGINE (LEVEL 6)
# -----------------------------
def match_bank_to_students(bank_df, students_df):

    bank = bank_df.copy()
    students = students_df.copy()

    students["norm_name"] = students["name"].fillna("").str.lower()

    def normalise(text):
        text = str(text).lower()
        text = re.sub(r"[^a-z0-9 ]", " ", text)
        return text

    bank["norm_text"] = (
        bank.get("description", "").fillna("").astype(str)
        + " "
        + bank.get("reference", "").fillna("").astype(str)
        + " "
        + bank.get("narrative", "").fillna("").astype(str)
    ).apply(normalise)

    bank["matched_student_id"] = None
    bank["match_confidence"] = 0.0

    for i, txn in bank.iterrows():

        best_score = 0
        best_student = None

        for _, student in students.iterrows():

            name = student["norm_name"]
            if not name:
                continue

            score = fuzz.partial_ratio(name, txn["norm_text"])

            if score > best_score:
                best_score = score
                best_student = student["student_id"]

        if best_score >= 80:
            bank.at[i, "matched_student_id"] = best_student
            bank.at[i, "match_confidence"] = best_score / 100

    return bank

# -----------------------------
# RECONCILIATION CORE
# -----------------------------
def reconcile(bank_df: pd.DataFrame,
              tracker_df: pd.DataFrame,
              students_df: pd.DataFrame) -> dict:
    """
    Returns full reconciliation view:
    - matched transactions
    - unmatched bank payments
    - tracker-only entries
    """

    bank = match_bank_to_students(bank_df, students_df)

    # -----------------------------
    # BANK AGGREGATION
    # -----------------------------
    bank_paid = (
        bank.dropna(subset=["matched_student_id"])
        .groupby("matched_student_id", as_index=False)
        .agg(bank_total=("amount", "sum"))
    )

    # -----------------------------
    # TRACKER AGGREGATION
    # -----------------------------
    tracker_paid = (
        tracker_df.groupby("student_id", as_index=False)
        .agg(tracker_total=("amount", "sum"))
    )

    # -----------------------------
    # MERGE VIEW
    # -----------------------------
    reconciliation = pd.merge(
        bank_paid,
        tracker_paid,
        left_on="matched_student_id",
        right_on="student_id",
        how="outer"
    )

    reconciliation["bank_total"] = reconciliation["bank_total"].fillna(0)
    reconciliation["tracker_total"] = reconciliation["tracker_total"].fillna(0)

    reconciliation["difference"] = reconciliation["bank_total"] - reconciliation["tracker_total"]

    reconciliation["status"] = reconciliation["difference"].apply(
        lambda x: "MATCH" if x == 0 else "MISMATCH"
    )

    # -----------------------------
    # UNMATCHED BANK TXNS
    # -----------------------------
    unmatched_bank = bank[bank["matched_student_id"].isna()]

    return {
        "reconciliation": reconciliation,
        "unmatched_bank": unmatched_bank,
        "raw_bank": bank
    }
