"""
Universe Simulator - FarmHash64 (simplified)
Original pure-Python mixing for short keys.
"""

from __future__ import annotations

def _rot64(x: int, k: int) -> int:
    return ((x << k) | (x >> (64 - k))) & 0xFFFFFFFFFFFFFFFF

def farmhash64(data: bytes) -> int:
    length = len(data)
    if length == 0:
        return 0
    mul = 0x9ddfea08eb382d69
    a = int.from_bytes(data[:8].ljust(8, b"\x00"), "little")
    b = int.from_bytes(data[max(0, length-8):].rjust(8, b"\x00"), "little")
    a = (a + length) * mul
    a ^= _rot64(b, 37)
    b = (b + length) * mul
    b ^= _rot64(a, 25)
    a = (a + b) * mul
    a ^= a >> 47
    return a & 0xFFFFFFFFFFFFFFFF

if __name__ == "__main__":
    h = farmhash64(b"hello")
    assert isinstance(h, int)
    print("farmhash self-test passed", hex(h))
