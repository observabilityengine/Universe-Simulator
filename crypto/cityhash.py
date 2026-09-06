"""CityHash64 (simplified non-streaming pure-Python).

Complexity: O(n) for short inputs; this version targets short strings.
Not bit-identical to the original C++ CityHash for all lengths;
suitable for research hashing, not as a drop-in compatibility layer.
"""
from __future__ import annotations


def _rot64(x: int, k: int) -> int:
    return ((x << k) | (x >> (64 - k))) & 0xFFFFFFFFFFFFFFFF


def _shift_mix(val: int) -> int:
    return val ^ (val >> 47)


def cityhash64(data: bytes, seed: int = 0) -> int:
    """64-bit CityHash-style mix."""
    length = len(data)
    if length == 0:
        return seed & 0xFFFFFFFFFFFFFFFF
    mul = 0x9DDFEA08EB382D69
    a = (int.from_bytes(data[:8].ljust(8, b"\x00"), "little") + seed) & 0xFFFFFFFFFFFFFFFF
    b = int.from_bytes(data[max(0, length - 8) :].rjust(8, b"\x00")[-8:], "little") & 0xFFFFFFFFFFFFFFFF
    c = ((length + seed) * mul) & 0xFFFFFFFFFFFFFFFF
    a = (_shift_mix(a ^ b) * mul) & 0xFFFFFFFFFFFFFFFF
    b = (_shift_mix(b ^ c) * mul) & 0xFFFFFFFFFFFFFFFF
    return _shift_mix(a ^ b) & 0xFFFFFFFFFFFFFFFF


if __name__ == "__main__":
    assert cityhash64(b"") == 0
    h1 = cityhash64(b"hello")
    h2 = cityhash64(b"hello")
    assert h1 == h2
    assert cityhash64(b"hello") != cityhash64(b"world")
    assert cityhash64(b"a", seed=1) != cityhash64(b"a", seed=2)
    print("cityhash self-tests passed")
