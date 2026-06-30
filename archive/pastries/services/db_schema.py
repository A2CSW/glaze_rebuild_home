from services.db import get_conn

def init_extended_schema():
    conn = get_conn()
    c = conn.cursor()

    # staff users
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        role TEXT
    )
    """)

    # attendance (register replacement)
    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        class_id TEXT,
        date TEXT,
        present INTEGER,
        marked_by TEXT
    )
    """)

    conn.commit()
    conn.close()
