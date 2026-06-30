import pandas as pd

# -----------------------------
# LOADERS
# -----------------------------

def load_register(path):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()

    # enforce string identity
    if "student_id" not in df.columns:
        raise ValueError("Register must contain 'student_id' column")

    df["student_id"] = df["student_id"].astype(str)
    df["status"] = df["status"].str.upper()

    return df


def load_tracker(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    if "student_id" not in df.columns:
        raise ValueError("Tracker must contain 'student_id' column")

    df["student_id"] = df["student_id"].astype(str)

    return df


# -----------------------------
# CORE LOGIC
# -----------------------------

def get_current_students(register_df):
    """
    CURRENT overrides everything.
    """
    df = register_df.copy()

    current = df[df["status"] == "CURRENT"]

    # deduplicate (critical rule)
    current = current.drop_duplicates(subset=["student_id"])

    return current


def build_payment_matrix(register_df, tracker_df):
    """
    One row per student, alphabetical, no duplicates.
    """

    reg = register_df.copy()
    pay = tracker_df.copy()

    # ensure numeric safety
    pay["amount"] = pd.to_numeric(pay["amount"], errors="coerce").fillna(0)

    # aggregate monthly payments
    if "month" not in pay.columns:
        raise ValueError("Tracker must contain 'month' column")

    pivot = pay.pivot_table(
        index=["student_id"],
        columns="month",
        values="amount",
        aggfunc="sum",
        fill_value=0
    ).reset_index()

    # merge names
    merged = reg[["student_id", "first_name", "last_name"]].drop_duplicates()

    merged = merged.merge(pivot, on="student_id", how="left")

    merged["full_name"] = (
        merged["first_name"].fillna("") + " " + merged["last_name"].fillna("")
    ).str.strip()

    merged = merged.sort_values("full_name")

    return merged


# -----------------------------
# PUBLIC API (GLAZE USES ONLY THIS)
# -----------------------------

def build_glaze_outputs(register_path, tracker_path):
    register = load_register(register_path)
    tracker = load_tracker(tracker_path)

    current_students = get_current_students(register)
    payment_matrix = build_payment_matrix(register, tracker)

    return current_students, payment_matrix
