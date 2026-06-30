from __future__ import annotations
import pandas as pd
from core.data_store import load_table, save_table
from core.exceptions import ServiceError
from core.upsert import update_rows
from core.validation import validate_table
from services.id_service import generate_id
VALID_REVIEW_STATUSES = {"Unreviewed", "Matched", "Approved", "Rejected"}
def list_bank_transactions() -> pd.DataFrame:
    return load_table("bank_transactions")
def create_bank_transaction(
    date: str,
    description: str,
    amount: str,
    account: str = "",
    source_file: str = "",
    matched_student_id: str = "",
    matched_guardian_id: str = "",
    match_confidence: str = "",
    match_method: str = "",
    review_status: str = "Unreviewed",
    notes: str = "",
) -> dict[str, str]:
    date = date.strip()
    description = description.strip()
    amount = amount.strip()
    review_status = review_status.strip().title()
    if not date:
        raise ServiceError("date is required.")
    if not description:
        raise ServiceError("description is required.")
    if not amount:
        raise ServiceError("amount is required.")
    if review_status not in VALID_REVIEW_STATUSES:
        raise ServiceError(f"Invalid review status: {review_status}")
    transactions = load_table("bank_transactions")
    new_record = {
        "transaction_id": generate_id("BNK"),
        "date": date,
        "description": description,
        "amount": amount,
        "account": account.strip(),
        "source_file": source_file.strip(),
        "matched_student_id": matched_student_id.strip(),
        "matched_guardian_id": matched_guardian_id.strip(),
        "match_confidence": match_confidence.strip(),
        "match_method": match_method.strip(),
        "review_status": review_status,
        "notes": notes.strip(),
    }
    updated = pd.concat([transactions, pd.DataFrame([new_record])], ignore_index=True)
    clean = validate_table(updated, "bank_transactions")
    save_table("bank_transactions", clean)
    return new_record
def update_bank_transaction(
    transaction_id: str,
    date: str,
    description: str,
    amount: str,
    account: str = "",
    source_file: str = "",
    matched_student_id: str = "",
    matched_guardian_id: str = "",
    match_confidence: str = "",
    match_method: str = "",
    review_status: str = "Unreviewed",
    notes: str = "",
) -> dict[str, str]:
    transaction_id = transaction_id.strip()
    date = date.strip()
    description = description.strip()
    amount = amount.strip()
    review_status = review_status.strip().title()
    if not transaction_id:
        raise ServiceError("transaction_id is required.")
    if not date:
        raise ServiceError("date is required.")
    if not description:
        raise ServiceError("description is required.")
    if not amount:
        raise ServiceError("amount is required.")
    if review_status not in VALID_REVIEW_STATUSES:
        raise ServiceError(f"Invalid review status: {review_status}")
    transactions = load_table("bank_transactions")
    updated = update_rows(
        transactions,
        {"transaction_id": transaction_id},
        {
            "date": date,
            "description": description,
            "amount": amount,
            "account": account.strip(),
            "source_file": source_file.strip(),
            "matched_student_id": matched_student_id.strip(),
            "matched_guardian_id": matched_guardian_id.strip(),
            "match_confidence": match_confidence.strip(),
            "match_method": match_method.strip(),
            "review_status": review_status,
            "notes": notes.strip(),
        },
    )
    clean = validate_table(updated, "bank_transactions")
    save_table("bank_transactions", clean)
    row = clean[clean["transaction_id"].astype(str).str.strip() == transaction_id].iloc[0]
    return row.to_dict()
