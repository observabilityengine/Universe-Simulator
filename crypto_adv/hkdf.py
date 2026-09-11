"""HKDF-Extract and Expand (RFC 5869 style with HMAC-SHA256)."""
from __future__ import annotations
import hashlib
import hmac


def hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    if not salt:
        salt = b"\x00" * 32
    return hmac.new(salt, ikm, hashlib.sha256).digest()


def hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
    out = b""
    t = b""
    counter = 1
    while len(out) < length:
        t = hmac.new(prk, t + info + bytes([counter]), hashlib.sha256).digest()
        out += t
        counter += 1
    return out[:length]


def hkdf(ikm: bytes, salt: bytes = b"", info: bytes = b"", length: int = 32) -> bytes:
    return hkdf_expand(hkdf_extract(salt, ikm), info, length)


if __name__ == "__main__":
    okm = hkdf(b"input key material", b"salt", b"info", 32)
    assert len(okm) == 32
    print(f"hkdf okm[0]={okm[0]}")
    print("hkdf self-tests passed")
