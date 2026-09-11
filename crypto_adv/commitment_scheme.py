"""Hash-based commitment scheme."""
from __future__ import annotations
import hashlib


def commit(value: bytes, randomness: bytes) -> bytes:
    return hashlib.sha256(value + b"|" + randomness).digest()


def open_commitment(commitment: bytes, value: bytes, randomness: bytes) -> bool:
    expected = commit(value, randomness)
    if len(commitment) != len(expected):
        return False
    result = 0
    for x, y in zip(commitment, expected):
        result |= x ^ y
    return result == 0


if __name__ == "__main__":
    r = b"randomness16byte"
    c = commit(b"secret", r)
    assert open_commitment(c, b"secret", r)
    assert not open_commitment(c, b"wrong", r)
    print("commitment_scheme self-tests passed")
