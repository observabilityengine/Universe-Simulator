"""
Module 61 – Password Hashing
PBKDF2-HMAC-SHA256 with salt and verification.
Complete implementation using only hashlib.
"""

from __future__ import annotations
import hashlib
import hmac
import os


def hash_password(password: str, iterations: int = 100_000) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, iter_str, salt_hex, hash_hex = stored.split("$")
        if algo != "pbkdf2_sha256":
            return False
        iterations = int(iter_str)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
        return hmac.compare_digest(dk, expected)
    except Exception:
        return False


if __name__ == "__main__":
    print("Testing Password Hashing...")
    h = hash_password("correct horse battery staple")
    print(f"  Hash: {h[:50]}...")
    print(f"  Verify correct: {verify_password('correct horse battery staple', h)}")
    print(f"  Verify wrong:   {verify_password('wrong password', h)}")
    print("Password Hashing module OK.")
