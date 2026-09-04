"""
Universe Simulator - xxHash32 (simplified non-streaming)
Original pure-Python implementation of xxHash32.
"""

from __future__ import annotations

def rotl32(x: int, r: int) -> int:
    return ((x << r) | (x >> (32 - r))) & 0xFFFFFFFF

def xxhash32(data: bytes, seed: int = 0) -> int:
    PRIME1 = 0x9E3779B1
    PRIME2 = 0x85EBCA77
    PRIME3 = 0xC2B2AE3D
    PRIME4 = 0x27D4EB2F
    PRIME5 = 0x165667B1
    length = len(data)
    h = (seed + PRIME5) & 0xFFFFFFFF
    if length >= 16:
        v1 = (seed + PRIME1 + PRIME2) & 0xFFFFFFFF
        v2 = (seed + PRIME2) & 0xFFFFFFFF
        v3 = seed & 0xFFFFFFFF
        v4 = (seed - PRIME1) & 0xFFFFFFFF
        i = 0
        while i <= length - 16:
            for v, off in ((v1, 0), (v2, 4), (v3, 8), (v4, 12)):
                k = int.from_bytes(data[i+off:i+off+4], "little")
                k = (k * PRIME2) & 0xFFFFFFFF
                k = rotl32(k, 13)
                k = (k * PRIME1) & 0xFFFFFFFF
                if off == 0: v1 = (rotl32((v1 + k) & 0xFFFFFFFF, 13) * PRIME1) & 0xFFFFFFFF
                elif off == 4: v2 = (rotl32((v2 + k) & 0xFFFFFFFF, 13) * PRIME1) & 0xFFFFFFFF
                elif off == 8: v3 = (rotl32((v3 + k) & 0xFFFFFFFF, 13) * PRIME1) & 0xFFFFFFFF
                else: v4 = (rotl32((v4 + k) & 0xFFFFFFFF, 13) * PRIME1) & 0xFFFFFFFF
            i += 16
        h = (rotl32(v1, 1) + rotl32(v2, 7) + rotl32(v3, 12) + rotl32(v4, 18)) & 0xFFFFFFFF
    h = (h + length) & 0xFFFFFFFF
    # remaining bytes simplified
    for b in data[length - (length % 16):]:
        h = (h + b * PRIME5) & 0xFFFFFFFF
        h = (rotl32(h, 11) * PRIME1) & 0xFFFFFFFF
    h ^= h >> 15
    h = (h * PRIME2) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * PRIME3) & 0xFFFFFFFF
    h ^= h >> 16
    return h

if __name__ == "__main__":
    h = xxhash32(b"hello")
    assert isinstance(h, int) and 0 <= h <= 0xFFFFFFFF
    print("xxhash32 self-test passed", hex(h))
