"""
Universe Simulator - CityHash64 (simplified non-streaming)
Original pure-Python port of key mixing steps.
"""

from __future__ import annotations

def _rot64(x: int, k: int) -> int:
    return ((x << k) | (x >> (64 - k))) & 0xFFFFFFFFFFFFFFFF

def _shift_mix(val: int) -> int:
    return val ^ (val >> 47)

def cityhash64(data: bytes, seed: int = 0) -> int:
    length = len(data)
    if length == 0:
        return seed
    # simplified for short strings
    mul = 0x9ddfea08eb382d69
    a = (int.from_bytes(data[:8].ljust(8, b"\x00"), "little") + seed) & 0xFFFFFFFFFFFFFFFF
    b = int.from_bytes(data[max(0, length-8):].ljust(8, b"\x00"), "little") & 0xFFFFFFFFFFFFFFFF
    c = ((length + seed) * mul) & 0xFFFFFFFFFFFFFFFF
    a = _shift_mix(a ^ b) * mul
    b = _shift_mix(b ^ c) * mul
    return _shift_mix(a ^ b) & 0xFFFFFFFFFFFFFFFF

if __name__ == "__main__":
    h = cityhash64(b"hello")
    assert isinstance(h, int)
    print("cityhash self-test passed", hex(h))
