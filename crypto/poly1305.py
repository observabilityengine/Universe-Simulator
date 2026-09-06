"""Poly1305 one-time authenticator (RFC 7539 style).

Complexity: O(n).
Pure-Python implementation for research / verification.
Key must be 32 bytes (r || s). Not a general-purpose MAC without a unique key per message.
"""
from __future__ import annotations


def poly1305(msg: bytes, key: bytes) -> bytes:
    """Compute 16-byte Poly1305 tag."""
    if len(key) != 32:
        raise ValueError("key must be 32 bytes")
    r = int.from_bytes(key[:16], "little") & 0x0FFFFFFC0FFFFFFC0FFFFFFC0FFFFFFF
    s = int.from_bytes(key[16:], "little")
    h = 0
    p = (1 << 130) - 5
    for i in range(0, len(msg), 16):
        block = msg[i : i + 16]
        n = int.from_bytes(block + b"\x01", "little")
        h = ((h + n) * r) % p
    h = (h + s) % (1 << 128)
    return h.to_bytes(16, "little")


if __name__ == "__main__":
    key = bytes(range(32))
    tag1 = poly1305(b"hello", key)
    assert len(tag1) == 16
    tag2 = poly1305(b"hello", key)
    assert tag1 == tag2
    tag3 = poly1305(b"world", key)
    assert tag1 != tag3
    try:
        poly1305(b"x", b"short")
        assert False
    except ValueError:
        pass
    # empty message
    assert len(poly1305(b"", key)) == 16
    print("poly1305 self-tests passed")
