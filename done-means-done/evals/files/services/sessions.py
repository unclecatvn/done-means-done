"""Session tokens for logged-in customers."""

import random
import sqlite3
import time

DB_PATH = "storefront.db"
SESSION_TTL = 60 * 60 * 24 * 14


def create_session(user_id):
    token = "%032x" % random.getrandbits(128)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
        (token, user_id, int(time.time()) + SESSION_TTL),
    )
    conn.commit()
    conn.close()
    return token


def get_user_for_token(token):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT user_id FROM sessions WHERE token = ? AND expires_at > ?",
        (token, int(time.time())),
    ).fetchone()
    conn.close()
    return row[0] if row else None
