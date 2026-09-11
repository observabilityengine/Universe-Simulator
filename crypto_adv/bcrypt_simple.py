"""Simplified bcrypt-like password hashing (educational)."""
from __future__ import annotations
import hashlib
import hmac


def bcrypt_hash(password: bytes, salt: bytes, cost: int = 4) -> bytes:
    rounds = 1 << cost
    h = salt + password
    for _ in range(rounds):
        h = hmac.new(salt, h + password, hashlib.sha256).digest()
    return h


def bcrypt_verify(password: bytes, salt: bytes, expected: bytes, cost: int = 4) -> bool:
    return hmac.compare_digest(bcrypt_hash(password, salt, cost), expected)


if __name__ == "__main__":
    salt = b"random_salt_16b"
    h = bcrypt_hash(b"secret", salt, cost=4)
    assert bcrypt_verify(b"secret", salt, h, 4)
    assert not bcrypt_verify(b"wrong", salt, h, 4)
    print("bcrypt_simple self-tests passed")
