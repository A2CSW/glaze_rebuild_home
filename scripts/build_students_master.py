import pandas as pd
import os
import glob

# ---------------------------------------------------
# ABSOLUTE DATA ROOT (LOCKED)
# ---------------------------------------------------
DATA_DIR = "/Users/stephenwoods/Documents/glaze/data"
OUTPUT_DIR = "/Users/stephenwoods/Documents/glaze/data/sqlite_ready"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("🔄 Processing register files from:", DATA_DIR)

# ---------------------------------------------------
# FIND REGISTER FILES (EXPLICIT PATTERN ONLY)
# ---------------------------------------------------
register_files = glob.glob(f"{DATA_DIR}/Register 25_26 - *.csv")

print(f"📁 Found {len(register_files)} register files")

all_records = []

# ---------------------------------------------------
# PROCESS EACH REGISTER FILE
# ---------------------------------------------------
for file_path in register_files:

    try:
        df = pd.read_csv(file_path, on_bad_lines='skip', encoding='utf-8')

        df.columns = [
            col.strip().replace('\n', ' ').replace('  ', ' ')
            for col in df.columns
        ]

        # Flexible column detection
        name_col = next((c for c in df.columns if 'name' in c.lower() or 'student' in c.lower()), None)
        dob_col = next((c for c in df.columns if 'dob' in c.lower() or 'birth' in c.lower()), None)
        status_col = next((c for c in df.columns if 'current' in c.lower() or 'former' in c.lower()), None)
        parent_col = next((c for c in df.columns if 'parent' in c.lower() or 'guardian' in c.lower()), None)
        mobile_col = next((c for c in df.columns if 'mobile' in c.lower() or 'phone' in c.lower()), None)

        if name_col and status_col:

            current = df[
                df[status_col].astype(str).str.contains("Current", case=False, na=False)
            ].copy()

            if not current.empty:

                current = current.rename(columns={
                    name_col: "full_name",
                    dob_col: "dob" if dob_col else "dob",
                    parent_col: "guardian_name" if parent_col else "guardian_name",
                    mobile_col: "guardian_mobile" if mobile_col else "guardian_mobile"
                })

                current["source_file"] = os.path.basename(file_path)

                all_records.append(current)

                print(f"✅ {os.path.basename(file_path)} → {len(current)} students")

    except Exception as e:
        print(f"⚠️ ERROR in {file_path}: {e}")

# ---------------------------------------------------
# COMBINE ALL DATA
# ---------------------------------------------------
if not all_records:
    raise Exception("No register data found. Check file structure.")

master = pd.concat(all_records, ignore_index=True)

# ---------------------------------------------------
# CLEANING
# ---------------------------------------------------
master["full_name"] = master["full_name"].astype(str).str.strip().str.title()

master = master.drop_duplicates(subset=["full_name", "dob"], keep="last")

# ---------------------------------------------------
# STABLE ID GENERATION
# ---------------------------------------------------
def make_student_id(row):
    name = str(row.get("full_name", "UNK")).split()[0][:4].upper()
    dob = str(row.get("dob", "")).replace("/", "")[-6:]
    return f"{name}{dob}"

master["student_id"] = master.apply(make_student_id, axis=1)

# ---------------------------------------------------
# FINAL STUDENTS TABLE
# ---------------------------------------------------
students_master = master[
    ["student_id", "full_name", "dob", "guardian_name", "guardian_mobile", "source_file"]
].copy()

students_path = f"{OUTPUT_DIR}/students_master.csv"
students_master.to_csv(students_path, index=False)

print("📊 Students written to:", students_path)
print("TOTAL STUDENTS:", len(students_master))

# ---------------------------------------------------
# ENROLLMENTS TABLE
# ---------------------------------------------------
enrollments = master[["student_id", "full_name", "source_file"]].copy()

enrollments["class_name"] = enrollments["source_file"].str.replace(
    "Register 25_26 - ", "", regex=False
).str.replace(".csv", "", regex=False).str.strip()

enrollments_path = f"{OUTPUT_DIR}/enrollments.csv"
enrollments.to_csv(enrollments_path, index=False)

print("📊 Enrollments written to:", enrollments_path)
print("TOTAL ENROLLMENTS:", len(enrollments))

print("✅ DONE")
