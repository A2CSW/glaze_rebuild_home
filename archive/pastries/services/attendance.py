import sqlite3

DB_PATH = "data/pastries.db"

def attendance_exists(student_id, class_id, date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT 1
        FROM attendance
        WHERE student_id = ?
        AND class_id = ?
        AND date = ?
        LIMIT 1
    """, (student_id, class_id, date))

    exists = c.fetchone() is not None

    conn.close()

    return exists


def save_attendance(student_id, class_id, date, present, marked_by):
    if attendance_exists(student_id, class_id, date):
        return False

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO attendance
        (student_id, class_id, date, present, marked_by)
        VALUES (?, ?, ?, ?, ?)
    """, (
        student_id,
        class_id,
        date,
        int(present),
        marked_by
    ))

    conn.commit()
    conn.close()

    return True


def get_attendance():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT
            student_id,
            class_id,
            date,
            present,
            marked_by
        FROM attendance
        ORDER BY date DESC
    """)

    rows = c.fetchall()

    conn.close()

    return rows
