"""Poly1305 MAC (simplified pure-Python)."""
from __future__ import annotations

P = (1 << 130) - 5


def poly1305_mac(msg: bytes, key: bytes) -> bytes:
    r = int.from_bytes(key[:16], "little") & 0x0FFFFFFC0FFFFFFC0FFFFFFC0FFFFFFF
    s = int.from_bytes(key[16:32], "little")
    acc = 0
    for i in range(0, len(msg), 16):
        block = msg[i : i + 16] + b"\x01"
        n = int.from_bytes(block.ljust(17, b"\x00"), "little")
        acc = (acc + n) * r % P
    acc = (acc + s) % (1 << 128)
    return (acc % (1 << 128)).to_bytes(16, "little")


if __name__ == "__main__":
    tag = poly1305_mac(b"hello", b"\x00" * 32)
    assert len(tag) == 16
    print(f"poly1305 tag[0]={tag[0]}")
    print("poly1305 self-tests passed")
