import pandas as pd
import hashlib

TRACKER_FILE = "migration/output/tanya_tracker_clean.csv"
OUT_FILE = "migration/output/student_master.csv"


def make_id(name) -> str:
    if pd.isna(name):
        return "unknown"

    name = str(name).lower().strip()

    if not name:
        return "unknown"

    return hashlib.md5(name.encode()).hexdigest()[:10]


def load():
    return pd.read_csv(TRACKER_FILE)


def build_students(df):
    df = df.copy()

    df["student_name"] = (
        df["first_name"].astype(str).str.strip()
        + " "
        + df["last_name"].astype(str).str.strip()
    )

    students = df[["student_name"]].drop_duplicates()

    students["student_id"] = students["student_name"].apply(make_id)

    # minimal stable attributes
    students["status"] = "active"  # placeholder for now

    return students


def main():
    df = load()
    students = build_students(df)

    print("ROWS:", len(students))
    print(students.head(20))

    students.to_csv(OUT_FILE, index=False)
    print("Saved →", OUT_FILE)


if __name__ == "__main__":
    main()
