from services.db import get_conn
from datetime import datetime

def log_action(action, entity, entity_id):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        INSERT INTO audit_log (action, entity, entity_id, timestamp)
        VALUES (?, ?, ?, ?)
    """, (action, entity, entity_id, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def get_logs():
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM audit_log ORDER BY id DESC")
    rows = c.fetchall()

    conn.close()
    return rows
