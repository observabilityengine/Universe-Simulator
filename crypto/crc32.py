"""
Universe Simulator - CRC-32 (IEEE)
Original table-driven implementation.
"""

from __future__ import annotations

def _make_table() -> list:
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
    crc = 0xFFFFFFFF
    for b in data:
        crc = _TABLE[(crc ^ b) & 0xFF] ^ (crc >> 8)
    return crc ^ 0xFFFFFFFF

if __name__ == "__main__":
    assert crc32(b"123456789") == 0xCBF43926
    print("crc32 self-test passed")
