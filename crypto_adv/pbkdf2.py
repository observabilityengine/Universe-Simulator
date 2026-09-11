"""PBKDF2-HMAC-SHA256."""
from __future__ import annotations
import hashlib
import hmac


def pbkdf2(password: bytes, salt: bytes, iterations: int = 1000, dklen: int = 32) -> bytes:
    def F(i):
        u = hmac.new(password, salt + i.to_bytes(4, "big"), hashlib.sha256).digest()
        result = u
        for _ in range(iterations - 1):
            u = hmac.new(password, u, hashlib.sha256).digest()
            result = bytes(a ^ b for a, b in zip(result, u))
        return result
    out = b""
    block = 1
    while len(out) < dklen:
        out += F(block)
        block += 1
    return out[:dklen]


if __name__ == "__main__":
    dk = pbkdf2(b"password", b"salt", 10, 16)
    assert len(dk) == 16
    print(f"pbkdf2 dk[0]={dk[0]}")
    print("pbkdf2 self-tests passed")
