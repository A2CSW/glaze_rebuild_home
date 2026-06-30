import pandas as pd

BANK_FILE = "migration/output/transactions_clean.csv"
STUDENTS_FILE = "migration/output/student_master.csv"
OVERRIDES_FILE = "migration/manual/manual_payment_overrides.csv"
OUT_FILE = "migration/output/payments_resolved.csv"


def load():
    bank = pd.read_csv(BANK_FILE)
    students = pd.read_csv(STUDENTS_FILE)

    try:
        overrides = pd.read_csv(OVERRIDES_FILE)
    except Exception:
        overrides = pd.DataFrame(
            columns=["bank_reference", "decision", "student_id", "notes"]
        )

    return bank, students, overrides


def match_student(row, students):
    desc = str(row.get("transaction description", "")).lower()

    for _, s in students.iterrows():
        sid = str(s.get("student_id", "")).lower()

        if sid and sid in desc:
            return s["student_id"]

    for _, s in students.iterrows():
        name = str(s.get("student_name", "")).lower()

        if name and name in desc:
            return s["student_id"]

    return None


def main():
    bank, students, overrides = load()

    override_lookup = {}

    for _, row in overrides.iterrows():
        override_lookup[str(row["bank_reference"]).strip()] = row

    results = []

    for _, row in bank.iterrows():

        bank_ref = str(row.get("transaction description", "")).strip()

        if bank_ref in override_lookup:

            o = override_lookup[bank_ref]

            results.append({
                "date": row.get("transaction date"),
                "amount": row.get("amount_signed"),
                "bank_reference": bank_ref,
                "student_id": o.get("student_id"),
                "status": o.get("decision"),
                "source": "manual_override",
                "notes": o.get("notes")
            })

            continue

        student_id = match_student(row, students)

        results.append({
            "date": row.get("transaction date"),
            "amount": row.get("amount_signed"),
            "bank_reference": bank_ref,
            "student_id": student_id,
            "status": "matched" if student_id else "unmatched",
            "source": "auto_match",
            "notes": ""
        })

    df = pd.DataFrame(results)

    print("TOTAL:", len(df))
    print("MATCHED:", (df["status"] == "matched").sum())
    print("UNMATCHED:", (df["status"] == "unmatched").sum())
    print("MANUAL:", (df["source"] == "manual_override").sum())

    df.to_csv(OUT_FILE, index=False)

    print("Saved →", OUT_FILE)


if __name__ == "__main__":
    main()
