"""Bit packing / unpacking for unsigned integers into a bytearray.

Complexity: O(n) for n values.
Packs width-bit integers into a compact byte buffer. Original implementation.
"""
from __future__ import annotations

from typing import List


def bitpack(values: List[int], width: int) -> bytes:
    """Pack integers in [0, 2^width) into bytes."""
    if width < 1 or width > 64:
        raise ValueError("width must be in 1..64")
    if not values:
        return b""
    mask = (1 << width) - 1
    total_bits = len(values) * width
    out = bytearray((total_bits + 7) // 8)
    bit_pos = 0
    for v in values:
        if v < 0 or v > mask:
            raise ValueError(f"value {v} out of range for width {width}")
        for b in range(width):
            if v & (1 << b):
                byte_i = bit_pos // 8
                out[byte_i] |= 1 << (bit_pos % 8)
            bit_pos += 1
    return bytes(out)


def bitunpack(data: bytes, width: int, count: int) -> List[int]:
    """Unpack count width-bit integers from data."""
    if width < 1 or width > 64:
        raise ValueError("width must be in 1..64")
    result: List[int] = []
    bit_pos = 0
    for _ in range(count):
        v = 0
        for b in range(width):
            byte_i = bit_pos // 8
            if byte_i >= len(data):
                raise ValueError("insufficient data")
            if data[byte_i] & (1 << (bit_pos % 8)):
                v |= 1 << b
            bit_pos += 1
        result.append(v)
    return result


if __name__ == "__main__":
    vals = [0, 1, 2, 3, 7]
    packed = bitpack(vals, 3)
    assert bitunpack(packed, 3, 5) == vals
    assert bitpack([], 8) == b""
    assert bitunpack(bitpack([255], 8), 8, 1) == [255]
    try:
        bitpack([8], 3)
        assert False
    except ValueError:
        pass
    print("bitpack self-tests passed")
