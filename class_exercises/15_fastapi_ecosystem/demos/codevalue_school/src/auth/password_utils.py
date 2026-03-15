import base64
import hashlib
import hmac
import os

SALT_LENGTH = 32
PBKDF2_ITERATIONS = 260000


def hash_password(password: str) -> str:
    salt = os.urandom(SALT_LENGTH)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return base64.b64encode(salt + dk).decode("ascii")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    raw = base64.b64decode(hashed_password.encode("ascii"))
    salt = raw[:SALT_LENGTH]
    stored = raw[SALT_LENGTH:]
    dk = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return hmac.compare_digest(dk, stored)
