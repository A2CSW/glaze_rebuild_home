import sqlite3

DB_PATH = "data/pastries.db"

def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT,
        entity TEXT,
        entity_id TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()
