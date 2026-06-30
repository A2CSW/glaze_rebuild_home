import pandas as pd

FILE = "migration/source_registers/Register 25_26.xlsx"


def extract_sheet(sheet_name):
    df = pd.read_excel(FILE, sheet_name=sheet_name)

    student_col = df.columns[0]

    meta_cols = [
        "DOB",
        "Parent/Carer",
        "Mobile",
        "Promo ",
        "Need to knows"
    ]

    date_cols = [c for c in df.columns if c not in meta_cols and c != student_col]

    records = []

    current_status = "active"

    for _, row in df.iterrows():
        student = row[student_col]

        # section switch
        if isinstance(student, str):
            if student.strip().lower() == "former":
                current_status = "former"
                continue

            if student.strip().lower() == "incident/accident form":
                continue

        if pd.isna(student):
            continue

        for col in date_cols:
            value = row[col]

            if pd.isna(value):
                continue

            value = str(value).strip()

            if value == "1.0":
                value = "1"
            if value == "0.0":
                value = "0"

            records.append({
                "student_name": student,
                "class_name": sheet_name,
                "date": col,
                "status": value,
                "section_status": current_status
            })

    return pd.DataFrame(records)


def extract_all():
    xls = pd.ExcelFile(FILE)

    all_data = []

    for sheet in xls.sheet_names:
        name = sheet.lower()

        if "archive" in name:
            continue
        if "student data" in name:
            continue
        if "no consent" in name:
            continue

        df = extract_sheet(sheet)
        all_data.append(df)

    return pd.concat(all_data, ignore_index=True)


if __name__ == "__main__":
    out = extract_all()

    print(out.head(30))
    print("\nROWS:", len(out))

    out.to_csv("migration/output/attendance_fact.csv", index=False)
    print("\nSaved → migration/output/attendance_fact.csv")
