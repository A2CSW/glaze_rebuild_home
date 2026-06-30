import bcrypt
from services.db import get_conn

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_user(username, password, role="staff"):
    conn = get_conn()
    c = conn.cursor()

    pw_hash = hash_password(password)

    c.execute("""
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    """, (username, pw_hash, role))

    conn.commit()
    conn.close()


def authenticate(username, password):
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT username, password_hash, role FROM users WHERE username = ?", (username,))
    row = c.fetchone()

    conn.close()

    if not row:
        return None

    username, pw_hash, role = row

    if verify_password(password, pw_hash):
        return {"username": username, "role": role}

    return None
