import pandas as pd
from pathlib import Path

from pathlib import Path

from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data" / "processed_data"

def load_students():
    return pd.read_csv(BASE / "1_students_master.csv")


def save_students(students):
    students.to_csv(
        BASE / "1_students_master.csv",
        index=False
    )


def load_payments():
    return pd.read_csv(BASE / "2_payments_master.csv")

def load_attendance():
    return pd.read_csv(BASE / "3_attendance_tracker.csv")

def load_medical():
    return pd.read_csv(BASE / "4_medical_and_permissions.csv")

def load_contacts():
    return pd.read_csv(BASE / "5_students_contacts.csv")

def load_memberships():
    return pd.read_csv(BASE / "6_memberships.csv")

def load_addons():
    return pd.read_csv(BASE / "7_student_addons.csv")

def load_all():
    students = load_students()

    payments = load_payments()

    months = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May"]

    for m in months:
        if m in payments.columns:
            payments[m] = pd.to_numeric(
                payments[m],
                errors="coerce"
            ).fillna(0)

    return (
        students,
        load_attendance(),
        payments,
        load_medical(),
        load_contacts(),
        load_memberships(),
        load_addons()
    )
