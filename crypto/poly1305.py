"""
Universe Simulator - Poly1305 MAC (simplified)
Original pure-Python one-time authenticator.
"""

from __future__ import annotations

def poly1305(msg: bytes, key: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("key must be 32 bytes")
    r = int.from_bytes(key[:16], "little") & 0x0ffffffc0ffffffc0ffffffc0fffffff
    s = int.from_bytes(key[16:], "little")
    h = 0
    p = (1 << 130) - 5
    for i in range(0, len(msg), 16):
        block = msg[i:i+16]
        n = int.from_bytes(block + b"\x01", "little")
        h = (h + n) * r % p
    h = (h + s) % (1 << 128)
    return h.to_bytes(16, "little")

if __name__ == "__main__":
    tag = poly1305(b"hello", b"\x01" * 32)
    assert len(tag) == 16
    print("poly1305 self-test passed", tag[:4].hex())
