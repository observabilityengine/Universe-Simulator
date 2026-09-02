"""
Universe Simulator - Run-Length Encoding
Original encode / decode.
"""

from __future__ import annotations

from typing import List, Tuple


def rle_encode(data: bytes) -> List[Tuple[int, int]]:
    if not data:
        return []
    result = []
    prev = data[0]
    count = 1
    for b in data[1:]:
        if b == prev and count < 255:
            count += 1
        else:
            result.append((prev, count))
            prev = b
            count = 1
    result.append((prev, count))
    return result


def rle_decode(encoded: List[Tuple[int, int]]) -> bytes:
    out = bytearray()
    for val, cnt in encoded:
        out.extend([val] * cnt)
    return bytes(out)


if __name__ == "__main__":
    original = b"AAABBCCCCD"
    enc = rle_encode(original)
    dec = rle_decode(enc)
    assert dec == original
    print("rle self-test passed", enc)
