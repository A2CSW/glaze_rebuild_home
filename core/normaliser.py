import pandas as pd
import hashlib


# -----------------------------
# ID GENERATION
# -----------------------------

def make_student_id(first_name, last_name, fallback=None):
    base = f"{str(first_name).strip().lower()}_{str(last_name).strip().lower()}"

    if base.strip("_") == "_":
        base = str(fallback).strip().lower()

    return hashlib.md5(base.encode()).hexdigest()[:10]


# -----------------------------
# CLEAN ROW VALIDATION
# -----------------------------

def is_valid_student_row(name):
    if pd.isna(name):
        return False

    name_str = str(name).strip().lower()

    if name_str == "":
        return False

    if name_str in ["nan", "none", "null"]:
        return False

    return True


# -----------------------------
# EXTRACT FROM SHEET
# -----------------------------

def extract_students_from_sheet(df, sheet_name):

    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()

    # find student column flexibly
    student_col = None

    for col in df.columns:
        if str(col).strip().lower() in ["student", "student name", "name", "student id"]:
            student_col = col
            break

    if student_col is None:
        return pd.DataFrame()

    raw_names = df[student_col]

    mask = raw_names.apply(is_valid_student_row)
    df = df[mask].copy()

    names = df[student_col].astype(str).str.strip().str.split(" ", n=1, expand=True)

    out = pd.DataFrame()
    out["first_name"] = names[0]
    out["last_name"] = names[1] if names.shape[1] > 1 else ""

    if "Current or former" in df.columns:
        out["status_raw"] = df["Current or former"]
    else:
        out["status_raw"] = "Current"

    out["source_sheet"] = sheet_name

    return out


# -----------------------------
# MAIN NORMALISER
# -----------------------------

def build_canonical_students(register_xlsx_path):

    xls = pd.ExcelFile(register_xlsx_path)

    all_students = []

    for sheet in xls.sheet_names:

        df = pd.read_excel(xls, sheet_name=sheet)

        extracted = extract_students_from_sheet(df, sheet)

        if not extracted.empty:
            extracted["sheet"] = sheet
            all_students.append(extracted)

    if not all_students:
        return pd.DataFrame(columns=[
            "student_id",
            "first_name",
            "last_name",
            "status"
        ])

    students = pd.concat(all_students, ignore_index=True)

    # -----------------------------
    # FINAL CLEANING STEP
    # -----------------------------

    students = students[
        students["first_name"].notna()
        & (students["first_name"].astype(str).str.strip() != "")
        & (students["first_name"].astype(str).str.lower() != "nan")
    ]

    # -----------------------------
    # STATUS NORMALISATION
    # -----------------------------

    students["status_raw"] = students["status_raw"].fillna("Current").astype(str).str.lower()

    students["status"] = students["status_raw"].apply(
        lambda x: "CURRENT" if "current" in x else "FORMER"
    )

    # -----------------------------
    # STUDENT ID
    # -----------------------------

    students["student_id"] = students.apply(
        lambda r: make_student_id(
            r["first_name"],
            r["last_name"],
            fallback=r["first_name"]
        ),
        axis=1
    )

    # -----------------------------
    # DEDUPLICATION
    # -----------------------------

    students = students.sort_values("status", ascending=False)
    students = students.drop_duplicates(subset=["student_id"], keep="first")

    return students.reset_index(drop=True)
