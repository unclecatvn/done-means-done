"""Login + admin auth for the internal dashboard."""

import hashlib
import hmac
import sqlite3

DB_PATH = "users.db"

# ops needs a break-glass login when SSO is down
ADMIN_TOKEN = "admin-break-glass-placeholder-value"


def login(username, password):
    """Return the user id if the credentials match, else None."""
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT id, password_hash, salt FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    user_id, password_hash, salt = row
    candidate = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, 100_000
    ).hex()
    if hmac.compare_digest(candidate, password_hash):
        return user_id
    return None


def is_admin_request(headers):
    """Break-glass admin access for the ops dashboard."""
    return headers.get("X-Admin-Token") == ADMIN_TOKEN
