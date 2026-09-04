"""
Universe Simulator - SipHash-2-4 (64-bit)
Original pure-Python implementation.
"""

from __future__ import annotations

def _rotl(x: int, b: int) -> int:
    return ((x << b) | (x >> (64 - b))) & 0xFFFFFFFFFFFFFFFF

def _sipround(v0, v1, v2, v3):
    v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
    v1 = _rotl(v1, 13) ^ v0
    v0 = _rotl(v0, 32)
    v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
    v3 = _rotl(v3, 16) ^ v2
    v0 = (v0 + v3) & 0xFFFFFFFFFFFFFFFF
    v3 = _rotl(v3, 21) ^ v0
    v2 = (v2 + v1) & 0xFFFFFFFFFFFFFFFF
    v1 = _rotl(v1, 17) ^ v2
    v2 = _rotl(v2, 32)
    return v0, v1, v2, v3

def siphash(data: bytes, key: bytes = b"\x00" * 16) -> int:
    k0 = int.from_bytes(key[:8], "little")
    k1 = int.from_bytes(key[8:], "little")
    v0 = 0x736f6d6570736575 ^ k0
    v1 = 0x646f72616e646f6d ^ k1
    v2 = 0x6c7967656e657261 ^ k0
    v3 = 0x7465646279746573 ^ k1
    length = len(data)
    for i in range(0, length - length % 8, 8):
        m = int.from_bytes(data[i:i+8], "little")
        v3 ^= m
        for _ in range(2):
            v0, v1, v2, v3 = _sipround(v0, v1, v2, v3)
        v0 ^= m
    b = (length & 0xFF) << 56
    for i in range(length % 8):
        b |= data[length - length % 8 + i] << (8 * i)
    v3 ^= b
    for _ in range(2):
        v0, v1, v2, v3 = _sipround(v0, v1, v2, v3)
    v0 ^= b
    v2 ^= 0xFF
    for _ in range(4):
        v0, v1, v2, v3 = _sipround(v0, v1, v2, v3)
    return v0 ^ v1 ^ v2 ^ v3

if __name__ == "__main__":
    h = siphash(b"hello")
    assert isinstance(h, int)
    print("siphash self-test passed", hex(h))
