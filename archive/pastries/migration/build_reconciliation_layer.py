import pandas as pd

BANK_FILE = "migration/output/transactions_clean.csv"
TRACKER_FILE = "migration/output/tanya_tracker_clean.csv"
STUDENT_FILE = "migration/output/student_master.csv"
OUT_FILE = "migration/output/reconciliation.csv"


def load():
    return (
        pd.read_csv(BANK_FILE),
        pd.read_csv(TRACKER_FILE),
        pd.read_csv(STUDENT_FILE)
    )


def build_tracker_students(tracker, students):
    df = tracker.copy()

    df["student_name"] = (
        df["first_name"].astype(str).str.strip()
        + " "
        + df["last_name"].astype(str).str.strip()
    )

    return df.merge(students, on="student_name", how="left")


def simple_match(bank, tracker):
    results = []

    for _, b in bank.iterrows():
        ref = str(b.get("transaction description", ""))

        best = None

        for _, t in tracker.iterrows():
            name = str(t.get("student_name", ""))

            if name.lower() in ref.lower():
                best = t["student_id"]
                break

        results.append({
            "bank_reference": ref,
            "matched_student_id": best,
            "matched": best is not None
        })

    return pd.DataFrame(results)


def main():
    bank, tracker, students = load()

    tracker = build_tracker_students(tracker, students)

    recon = simple_match(bank, tracker)

    print(recon.head(20))
    print("MATCHED:", recon["matched"].sum())

    recon.to_csv(OUT_FILE, index=False)
    print("Saved →", OUT_FILE)


if __name__ == "__main__":
    main()
