"""CRC-32 (IEEE / ISO 3309 / ITU-T V.42).

Complexity: O(n) with 256-entry table.
Matches the standard polynomial 0xEDB88320 (reflected).
"""
from __future__ import annotations


def _make_table() -> list[int]:
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xEDB88320
            else:
                crc >>= 1
        table.append(crc)
    return table


_TABLE = _make_table()


def crc32(data: bytes) -> int:
    """Return CRC-32 as unsigned 32-bit integer."""
    crc = 0xFFFFFFFF
    for b in data:
        crc = _TABLE[(crc ^ b) & 0xFF] ^ (crc >> 8)
    return (crc ^ 0xFFFFFFFF) & 0xFFFFFFFF


if __name__ == "__main__":
    # Standard check value
    assert crc32(b"123456789") == 0xCBF43926
    assert crc32(b"") == 0
    assert crc32(b"a") != crc32(b"b")
    # Idempotent
    assert crc32(b"hello") == crc32(b"hello")
    print("crc32 self-tests passed")
