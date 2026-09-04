"""
Universe Simulator - SpookyHash 32-bit (simplified)
Original pure-Python short-message mixing.
"""

from __future__ import annotations

def _rot32(x: int, k: int) -> int:
    return ((x << k) | (x >> (32 - k))) & 0xFFFFFFFF

def spookyhash32(data: bytes, seed: int = 0) -> int:
    length = len(data)
    h = (seed + length) & 0xFFFFFFFF
    for i in range(0, length - length % 4, 4):
        k = int.from_bytes(data[i:i+4], "little")
        k = (k * 0xcc9e2d51) & 0xFFFFFFFF
        k = _rot32(k, 15)
        k = (k * 0x1b873593) & 0xFFFFFFFF
        h ^= k
        h = _rot32(h, 13)
        h = (h * 5 + 0xe6546b64) & 0xFFFFFFFF
    # remainder
    k = 0
    rem = data[length - length % 4:]
    for i, b in enumerate(rem):
        k |= b << (8 * i)
    k = (k * 0xcc9e2d51) & 0xFFFFFFFF
    k = _rot32(k, 15)
    k = (k * 0x1b873593) & 0xFFFFFFFF
    h ^= k
    h ^= length
    h ^= h >> 16
    h = (h * 0x85ebca6b) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 0xc2b2ae35) & 0xFFFFFFFF
    h ^= h >> 16
    return h

if __name__ == "__main__":
    h = spookyhash32(b"hello")
    assert isinstance(h, int) and 0 <= h <= 0xFFFFFFFF
    print("spookyhash self-test passed", hex(h))
