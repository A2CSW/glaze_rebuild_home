import sqlite3

DB_PATH = "data/pastries.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS overrides (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scope TEXT,
        student_id TEXT NOT NULL,
        class_name TEXT,
        field TEXT NOT NULL,
        value TEXT NOT NULL,
        notes TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Overrides DB initialised")


if __name__ == "__main__":
    init_db()
