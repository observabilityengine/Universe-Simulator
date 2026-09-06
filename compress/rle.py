"""Run-Length Encoding (byte-oriented).

Complexity: O(n) encode and decode.
Produces (value, count) pairs with count in 1..255.
Handles empty input and long runs correctly.
"""
from __future__ import annotations

from typing import List, Tuple


def rle_encode(data: bytes) -> List[Tuple[int, int]]:
    """Encode bytes into list of (byte_value, run_length)."""
    if not data:
        return []
    result: List[Tuple[int, int]] = []
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
    """Decode (value, count) pairs back to bytes."""
    out = bytearray()
    for val, cnt in encoded:
        if not (0 <= val <= 255) or cnt < 1:
            raise ValueError("invalid RLE pair")
        out.extend([val] * cnt)
    return bytes(out)


if __name__ == "__main__":
    assert rle_encode(b"") == []
    assert rle_decode([]) == b""
    original = b"AAABBCCCCD"
    enc = rle_encode(original)
    assert rle_decode(enc) == original
    # single byte
    assert rle_decode(rle_encode(b"X")) == b"X"
    # max run 255
    long = bytes([7] * 300)
    enc2 = rle_encode(long)
    assert rle_decode(enc2) == long
    assert all(c <= 255 for _, c in enc2)
    # all distinct
    distinct = bytes(range(10))
    assert rle_decode(rle_encode(distinct)) == distinct
    print("rle self-tests passed")
