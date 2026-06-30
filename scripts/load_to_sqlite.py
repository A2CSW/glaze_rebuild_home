import sqlite3
import pandas as pd

# -----------------------------
# ABSOLUTE PATHS (LOCKED)
# -----------------------------
DB_PATH = "/Users/stephenwoods/Documents/glaze/data/glaze.db"

STUDENTS_PATH = "/Users/stephenwoods/Documents/glaze/data/sqlite_ready/students_master.csv"
ENROLLMENTS_PATH = "/Users/stephenwoods/Documents/glaze/data/sqlite_ready/enrollments.csv"

# -----------------------------
# CONNECT DATABASE
# -----------------------------
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# -----------------------------
# CREATE TABLES (IF NOT EXISTS)
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    full_name TEXT,
    dob TEXT,
    guardian_name TEXT,
    guardian_mobile TEXT,
    source_file TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
    student_id TEXT,
    full_name TEXT,
    source_file TEXT,
    class_name TEXT
)
""")

conn.commit()

# -----------------------------
# LOAD CLEAN DATA
# -----------------------------
students = pd.read_csv(STUDENTS_PATH)
enrollments = pd.read_csv(ENROLLMENTS_PATH)

# -----------------------------
# WRITE TO SQLITE (REPLACE MODE)
# -----------------------------
students.to_sql("students", conn, if_exists="replace", index=False)
enrollments.to_sql("enrollments", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

# -----------------------------
# OUTPUT CONFIRMATION
# -----------------------------
print("✅ SQLite load complete")
print("DB:", DB_PATH)
print("Students:", len(students))
print("Enrollments:", len(enrollments))
