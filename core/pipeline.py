import pandas as pd
from core.loaders import clean_students, clean_payments

def build_core_dataset(students_df, payments_df):
    students = clean_students(students_df)
    payments = clean_payments(payments_df)

    # aggregate payments per student
    summary = payments.groupby("student_id")["amount"].sum().reset_index()
    summary.columns = ["student_id", "total_paid"]

    merged = students.merge(summary, on="student_id", how="left")
    merged["total_paid"] = merged["total_paid"].fillna(0)

    return merged

