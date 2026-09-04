"""
Universe Simulator - MurmurHash3 32-bit
Original pure-Python implementation.
"""

from __future__ import annotations

def _rotl32(x: int, r: int) -> int:
    return ((x << r) | (x >> (32 - r))) & 0xFFFFFFFF

def murmur3_32(data: bytes, seed: int = 0) -> int:
    c1 = 0xcc9e2d51
    c2 = 0x1b873593
    h = seed & 0xFFFFFFFF
    length = len(data)
    for i in range(0, length - length % 4, 4):
        k = int.from_bytes(data[i:i+4], "little")
        k = (k * c1) & 0xFFFFFFFF
        k = _rotl32(k, 15)
        k = (k * c2) & 0xFFFFFFFF
        h ^= k
        h = _rotl32(h, 13)
        h = (h * 5 + 0xe6546b64) & 0xFFFFFFFF
    k = 0
    rem = length % 4
    if rem >= 3:
        k ^= data[length - rem + 2] << 16
    if rem >= 2:
        k ^= data[length - rem + 1] << 8
    if rem >= 1:
        k ^= data[length - rem]
        k = (k * c1) & 0xFFFFFFFF
        k = _rotl32(k, 15)
        k = (k * c2) & 0xFFFFFFFF
        h ^= k
    h ^= length
    h ^= h >> 16
    h = (h * 0x85ebca6b) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 0xc2b2ae35) & 0xFFFFFFFF
    h ^= h >> 16
    return h

if __name__ == "__main__":
    assert murmur3_32(b"") == 0
    h = murmur3_32(b"hello")
    assert isinstance(h, int) and 0 <= h <= 0xFFFFFFFF
    print("murmur3 self-test passed", hex(h))
