import base64
import hashlib
import hmac
import os
import secrets
import time
from typing import Optional

from app.database import get_connection

SECRET_KEY = os.getenv("SECRET_KEY", "troque-esta-chave-em-producao")


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000,
    ).hex()
    return f"{salt}${password_hash}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, password_hash = stored_hash.split("$", 1)
        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100_000,
        ).hex()
        return hmac.compare_digest(new_hash, password_hash)
    except Exception:
        return False


def create_user(display_name: str, username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    password_hash = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (display_name, username, password_hash) VALUES (?, ?, ?)",
            (display_name.strip(), username.strip().lower(), password_hash),
        )
        conn.commit()
        return cursor.lastrowid
    except Exception:
        return None
    finally:
        conn.close()


def authenticate_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username.strip().lower(),))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    return user


def get_user_by_id(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def sign_value(value: str) -> str:
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        value.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    raw = f"{value}.{signature}"
    return base64.urlsafe_b64encode(raw.encode("utf-8")).decode("utf-8")


def unsign_value(signed_value: str) -> Optional[str]:
    try:
        decoded = base64.urlsafe_b64decode(signed_value.encode("utf-8")).decode("utf-8")
        value, signature = decoded.rsplit(".", 1)
        expected_signature = hmac.new(
            SECRET_KEY.encode("utf-8"),
            value.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            return None

        return value
    except Exception:
        return None


def create_session_token(user_id: int) -> str:
    timestamp = int(time.time())
    return sign_value(f"{user_id}:{timestamp}")


def get_current_user(request):
    token = request.cookies.get("healthnews_session")

    if not token:
        return None

    value = unsign_value(token)

    if not value:
        return None

    try:
        user_id_str, _timestamp = value.split(":", 1)
        return get_user_by_id(int(user_id_str))
    except Exception:
        return None
