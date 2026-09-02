"""
Module 71 – HMAC Authentication
HMAC-SHA256 message authentication + constant-time verify.
Complete implementation.
"""

from __future__ import annotations
import hashlib
import hmac
import os


def generate_key(length: int = 32) -> bytes:
    return os.urandom(length)


def sign(message: bytes, key: bytes) -> bytes:
    return hmac.new(key, message, hashlib.sha256).digest()


def verify(message: bytes, key: bytes, signature: bytes) -> bool:
    expected = sign(message, key)
    return hmac.compare_digest(expected, signature)


def sign_hex(message: str, key: bytes) -> str:
    return sign(message.encode(), key).hex()


def verify_hex(message: str, key: bytes, signature_hex: str) -> bool:
    try:
        sig = bytes.fromhex(signature_hex)
    except ValueError:
        return False
    return verify(message.encode(), key, sig)


if __name__ == "__main__":
    print("Testing HMAC Authentication...")
    key = generate_key()
    msg = b"transfer 100 USD to account 42"
    sig = sign(msg, key)
    print(f"  Signature: {sig.hex()[:32]}...")
    print(f"  Verify OK: {verify(msg, key, sig)}")
    print(f"  Verify tampered: {verify(msg + b'x', key, sig)}")
    print(f"  Hex round-trip: {verify_hex('hello', key, sign_hex('hello', key))}")
    print("HMAC Authentication module OK.")
