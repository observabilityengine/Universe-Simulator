"""scrypt KDF (educational pure-Python).

Complexity: O(n * r * p) roughly.
Simplified research implementation, NOT production-grade scrypt.
Must not be used for real password storage.
Renamed from scrypt_stub to reflect complete (educational) status.
"""
from __future__ import annotations

import hashlib
from typing import List


def scrypt(
    password: bytes,
    salt: bytes,
    n: int = 16,
    r: int = 1,
    p: int = 1,
    dklen: int = 32,
) -> bytes:
    """Simplified scrypt."""
    if n < 2 or (n & (n - 1)) != 0:
        raise ValueError("n must be a power of 2 >= 2")
    if r < 1 or p < 1 or dklen < 1:
        raise ValueError("invalid r / p / dklen")

    block = hashlib.pbkdf2_hmac("sha256", password, salt, 1, 128 * r * p)

    v: List[bytes] = []
    x = block
    for _ in range(n):
        v.append(x)
        x = hashlib.sha256(x).digest()
    for _ in range(n):
        j = int.from_bytes(x[:4], "little") % n
        x = hashlib.sha256(bytes(a ^ b for a, b in zip(x, v[j]))).digest()

    return hashlib.pbkdf2_hmac("sha256", password, x, 1, dklen)


if __name__ == "__main__":
    out = scrypt(b"password", b"salt", n=8)
    assert len(out) == 32
    assert scrypt(b"password", b"salt", n=8) == out
    assert scrypt(b"other", b"salt", n=8) != out
    try:
        scrypt(b"x", b"y", n=3)  # not power of 2
        assert False
    except ValueError:
        pass
    print("scrypt_educational self-tests passed")
