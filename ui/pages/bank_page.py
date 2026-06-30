from __future__ import annotations
import streamlit as st
from core.exceptions import ServiceError
from services.bank_service import create_bank_transaction, update_bank_transaction
from services.query_service import (
    get_bank_transactions_view,
    get_guardians_view,
    get_students_view,
)
def render_bank_page() -> None:
    st.header("Bank Transactions")
    st.caption("Foundation bank ledger page. Import/matching comes next.")
    students = get_students_view()
    guardians = get_guardians_view()
    student_options = [""]
    student_labels = {"": "(No matched student)"}
    if not students.empty:
        for _, row in students.iterrows():
            student_id = str(row["student_id"]).strip()
            full_name = str(row["full_name"]).strip()
            student_options.append(student_id)
            student_labels[student_id] = f"{full_name} ({student_id})"
    guardian_options = [""]
    guardian_labels = {"": "(No matched guardian)"}
    if not guardians.empty:
        for _, row in guardians.iterrows():
            guardian_id = str(row["guardian_id"]).strip()
            guardian_name = str(row["guardian_name"]).strip()
            guardian_options.append(guardian_id)
            guardian_labels[guardian_id] = f"{guardian_name} ({guardian_id})"
    with st.expander("Add Bank Transaction", expanded=False):
        with st.form("add_bank_transaction_form", clear_on_submit=True):
            date = st.text_input("Date (YYYY-MM-DD)")
            description = st.text_input("Description")
            amount = st.text_input("Amount")
            account = st.text_input("Account")
            source_file = st.text_input("Source File")
            matched_student_id = st.selectbox(
                "Matched Student",
                options=student_options,
                format_func=lambda x: student_labels.get(x, x),
            )
            matched_guardian_id = st.selectbox(
                "Matched Guardian",
                options=guardian_options,
                format_func=lambda x: guardian_labels.get(x, x),
            )
            match_confidence = st.text_input("Match Confidence")
            match_method = st.text_input("Match Method")
            review_status = st.selectbox(
                "Review Status",
                ["Unreviewed", "Matched", "Approved", "Rejected"],
                index=0,
            )
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Save Transaction")
        if submitted:
            try:
                record = create_bank_transaction(
                    date=date,
                    description=description,
                    amount=amount,
                    account=account,
                    source_file=source_file,
                    matched_student_id=matched_student_id,
                    matched_guardian_id=matched_guardian_id,
                    match_confidence=match_confidence,
                    match_method=match_method,
                    review_status=review_status,
                    notes=notes,
                )
                st.success(f"Bank transaction created: {record['transaction_id']}")
                st.rerun()
            except ServiceError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
    df = get_bank_transactions_view()
    st.write(f"Rows: {len(df)}")
    st.dataframe(df, use_container_width=True, hide_index=True)
    if df.empty:
        return
    st.subheader("Edit Existing Bank Transaction")
    tx_options = df["transaction_id"].astype(str).tolist()
    labels = {
        str(row["transaction_id"]): f"{row['date']} | {row['description']} ({row['transaction_id']})"
        for _, row in df.iterrows()
    }
    selected_tx_id = st.selectbox(
        "Select transaction",
        options=tx_options,
        format_func=lambda x: labels.get(x, x),
    )
    row = df[df["transaction_id"].astype(str) == selected_tx_id].iloc[0]
    current_student_id = str(row.get("matched_student_id", ""))
    current_guardian_id = str(row.get("matched_guardian_id", ""))
    student_index = student_options.index(current_student_id) if current_student_id in student_options else 0
    guardian_index = guardian_options.index(current_guardian_id) if current_guardian_id in guardian_options else 0
    statuses = ["Unreviewed", "Matched", "Approved", "Rejected"]
    current_status = str(row.get("review_status", "Unreviewed"))
    status_index = statuses.index(current_status) if current_status in statuses else 0
    with st.form("edit_bank_transaction_form"):
        date = st.text_input("Date (YYYY-MM-DD)", value=str(row.get("date", "")))
        description = st.text_input("Description", value=str(row.get("description", "")))
        amount = st.text_input("Amount", value=str(row.get("amount", "")))
        account = st.text_input("Account", value=str(row.get("account", "")))
        source_file = st.text_input("Source File", value=str(row.get("source_file", "")))
        matched_student_id = st.selectbox(
            "Matched Student",
            options=student_options,
            index=student_index,
            format_func=lambda x: student_labels.get(x, x),
        )
        matched_guardian_id = st.selectbox(
            "Matched Guardian",
            options=guardian_options,
            index=guardian_index,
            format_func=lambda x: guardian_labels.get(x, x),
        )
        match_confidence = st.text_input("Match Confidence", value=str(row.get("match_confidence", "")))
        match_method = st.text_input("Match Method", value=str(row.get("match_method", "")))
        review_status = st.selectbox("Review Status", statuses, index=status_index)
        notes = st.text_area("Notes", value=str(row.get("notes", "")))
        submitted = st.form_submit_button("Update Transaction")
    if submitted:
        try:
            record = update_bank_transaction(
                transaction_id=selected_tx_id,
                date=date,
                description=description,
                amount=amount,
                account=account,
                source_file=source_file,
                matched_student_id=matched_student_id,
                matched_guardian_id=matched_guardian_id,
                match_confidence=match_confidence,
                match_method=match_method,
                review_status=review_status,
                notes=notes,
            )
            st.success(f"Bank transaction updated: {record['transaction_id']}")
            st.rerun()
        except ServiceError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")
