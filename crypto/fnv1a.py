"""
Universe Simulator - FNV-1a 32-bit and 64-bit hash
Original implementation.
"""

from __future__ import annotations

def fnv1a_32(data: bytes) -> int:
    h = 0x811c9dc5
    for b in data:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h

def fnv1a_64(data: bytes) -> int:
    h = 0xcbf29ce484222325
    for b in data:
        h ^= b
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h

if __name__ == "__main__":
    assert fnv1a_32(b"") == 0x811c9dc5
    assert fnv1a_32(b"a") != fnv1a_32(b"b")
    print("fnv1a self-test passed", hex(fnv1a_32(b"hello")))
