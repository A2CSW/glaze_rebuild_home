import pandas as pd


def load_payments(path):
    df = pd.read_csv(path)
    df.columns = df.columns.astype(str).str.strip()
    return df


def build_name_lookup(students_df):
    students_df = students_df.copy()

    students_df["full_name"] = (
        students_df["first_name"].astype(str).str.strip().str.lower()
        + " "
        + students_df["last_name"].astype(str).str.strip().str.lower()
    )

    return dict(zip(students_df["full_name"], students_df["student_id"]))


def normalise_payments(payments_df, students_df):

    payments_df = payments_df.copy()
    payments_df.columns = payments_df.columns.astype(str).str.strip()

    name_to_id = build_name_lookup(students_df)

    payments_df["full_name"] = (
        payments_df["First Name"].astype(str).str.strip().str.lower()
        + " "
        + payments_df["Last Name"].astype(str).str.strip().str.lower()
    )

    payments_df["student_id"] = payments_df["full_name"].map(name_to_id)

    # keep only valid matches
    payments_df = payments_df.dropna(subset=["student_id"])

    return payments_df
