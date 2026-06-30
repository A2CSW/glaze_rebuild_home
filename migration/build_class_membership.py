import pandas as pd

INPUT_FILE = "migration/output/attendance_fact.csv"
OUTPUT_FILE = "migration/output/student_class_map.csv"


def build_class_membership():
    df = pd.read_csv(INPUT_FILE)

    # clean + stable types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["student_name"] = df["student_name"].astype(str).str.strip()

    # deterministic student_id (same logic as student_master v1)
    df["student_id"] = df["student_name"].apply(
        lambda x: __import__("hashlib").md5(x.encode("utf-8")).hexdigest()[:10]
    )

    # remove empty rows
    df = df[df["status"].notna()]

    grouped = df.groupby(["student_id", "class_name"]).agg(
        student_name=("student_name", "first"),
        first_seen=("date", "min"),
        last_seen=("date", "max"),
        attendance_count=("status", "count")
    ).reset_index()

    max_date = df["date"].max()

    grouped["active_flag"] = grouped["last_seen"].apply(
        lambda x: (max_date - x).days <= 60 if pd.notna(x) else False
    )

    return grouped


if __name__ == "__main__":
    out = build_class_membership()

    print(out.head(30))
    print("\nROWS:", len(out))

    out.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved → {OUTPUT_FILE}")
