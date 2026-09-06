"""FNV-1a 32-bit and 64-bit non-cryptographic hash.

Complexity: O(n).
Official FNV offset basis and prime constants.
"""
from __future__ import annotations


def fnv1a_32(data: bytes) -> int:
    """FNV-1a 32-bit. Returns unsigned 32-bit int."""
    h = 0x811C9DC5
    for b in data:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def fnv1a_64(data: bytes) -> int:
    """FNV-1a 64-bit. Returns unsigned 64-bit int."""
    h = 0xCBF29CE484222325
    for b in data:
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


if __name__ == "__main__":
    # Known empty hashes
    assert fnv1a_32(b"") == 0x811C9DC5
    assert fnv1a_64(b"") == 0xCBF29CE484222325
    # Deterministic and different for different inputs
    assert fnv1a_32(b"a") != fnv1a_32(b"b")
    assert fnv1a_64(b"a") != fnv1a_64(b"b")
    # Avalanche-ish: single bit flip changes hash
    assert fnv1a_32(b"hello") != fnv1a_32(b"hellp")
    # Stable across calls
    assert fnv1a_32(b"test") == fnv1a_32(b"test")
    print("fnv1a self-tests passed")
