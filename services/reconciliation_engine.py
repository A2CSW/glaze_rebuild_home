import pandas as pd
from rapidfuzz import fuzz
import re


# =============================================
# TEXT NORMALISER
# =============================================

def normalise(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return " ".join(text.split())

# =============================================
# BANK TRANSACTION CLEANER
# =============================================

def clean_bank_transactions(bank_df, barred_terms=None):

    bank = bank_df.copy()


    # -----------------------------------------
    # NORMALISE COLUMN NAMES
    # -----------------------------------------

    bank.columns = (
        bank.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )


    # -----------------------------------------
    # DESCRIPTION FIELD
    # -----------------------------------------

    text_columns = [
        "description",
        "transaction_description",
        "reference",
        "narrative"
    ]


    bank["description"] = ""


    for col in text_columns:

        if col in bank.columns:

            bank["description"] = (
                bank["description"]
                + " "
                + bank[col]
                .fillna("")
                .astype(str)
            )


    bank["description"] = (
        bank["description"]
        .str.strip()
    )


    # -----------------------------------------
    # AMOUNT FIELD
    # -----------------------------------------

    if "amount" not in bank.columns:

        amount_columns = [
            "credit_amount",
            "credit",
            "value"
        ]

        bank["amount"] = 0


        for col in amount_columns:

            if col in bank.columns:

                bank["amount"] = (
                    pd.to_numeric(
                        bank[col],
                        errors="coerce"
                    )
                    .fillna(0)
                )


    # -----------------------------------------
    # REMOVE MONEY OUT
    # -----------------------------------------

    bank = bank[
        bank["amount"] > 0
    ].copy()


    # -----------------------------------------
    # REMOVE BARRED ITEMS
    # -----------------------------------------

    if barred_terms:

        pattern = "|".join(barred_terms)

        bank = bank[
            ~bank["description"]
            .str.contains(
                pattern,
                case=False,
                na=False
            )
        ]


    return bank

# =============================================
# MATCH ONLY CURRENT STUDENTS
# =============================================

def match_bank_to_students(bank_df, students_df):

    bank = bank_df.copy()
    students = students_df.copy()


    # -----------------------------------------
    # ONLY CURRENT STUDENTS
    # -----------------------------------------

    if "status" in students.columns:

        students = students[
            students["status"] == "Current"
        ].copy()


    # -----------------------------------------
    # STUDENT NAME NORMALISATION
    # -----------------------------------------

    if "full_name" in students.columns:

        students["match_name"] = (
            students["full_name"]
            .fillna("")
            .astype(str)
            .str.upper()
        )

    elif "name" in students.columns:

        students["match_name"] = (
            students["name"]
            .fillna("")
            .astype(str)
            .str.upper()
        )

    else:

        students["match_name"] = ""


    # -----------------------------------------
    # BANK TEXT
    # -----------------------------------------

    bank["match_text"] = (
        bank["description"]
        .fillna("")
        .astype(str)
        .str.upper()
    )


    bank["matched_student_id"] = None
    bank["matched_name"] = ""
    bank["confidence"] = 0.0
    
    # -----------------------------------------
    # MATCH
    # -----------------------------------------

    from rapidfuzz import fuzz


    for i, transaction in bank.iterrows():

        best_score = 0
        best_student = None


        for _, student in students.iterrows():

            score = fuzz.partial_ratio(
                student["match_name"],
                transaction["match_text"]
            )


            if score > best_score:

                best_score = score
                best_student = student



        if best_student is not None and best_score >= 80:

            bank.at[
                i,
                "matched_student_id"
            ] = best_student["student_id"]


            bank.at[
                i,
                "matched_name"
            ] = best_student["match_name"]


            bank.at[
                i,
                "confidence"
            ] = best_score


    return bank

# =============================================
# CREATE TANYA REVIEW QUEUE
# =============================================

def build_payment_queue(
        bank_df,
        students_df,
        barred_terms=None):


    clean = clean_bank_transactions(
        bank_df,
        barred_terms
    )


    matched = match_bank_to_students(
        clean,
        students_df
    )


    return matched
