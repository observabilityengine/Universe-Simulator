"""Arithmetic coding (static model, integer implementation).

Complexity: O(n). Original fixed-precision arithmetic coder.
Encodes bytes; returns (bitstream as bytes, model freqs).
"""
from __future__ import annotations

from typing import Dict, List, Tuple


PRECISION = 32
FULL = 1 << PRECISION
HALF = FULL >> 1
QUARTER = HALF >> 1


def _build_cum(freqs: Dict[int, int]) -> Tuple[List[int], int]:
    cum = [0] * 257
    total = 0
    for i in range(256):
        total += freqs.get(i, 0)
        cum[i + 1] = total
    if total == 0:
        total = 1
    return cum, total


def arithmetic_encode(data: bytes) -> Tuple[bytes, Dict[int, int]]:
    """Encode data; returns (compressed bytes, frequency table)."""
    freqs: Dict[int, int] = {}
    for b in data:
        freqs[b] = freqs.get(b, 0) + 1
    if not data:
        return b"", freqs
    cum, total = _build_cum(freqs)
    low, high = 0, FULL - 1
    pending = 0
    out_bits: List[int] = []

    def emit_bit(bit: int) -> None:
        nonlocal pending
        out_bits.append(bit)
        while pending:
            out_bits.append(1 - bit)
            pending -= 1

    for b in data:
        range_ = high - low + 1
        high = low + (range_ * cum[b + 1]) // total - 1
        low = low + (range_ * cum[b]) // total
        while True:
            if high < HALF:
                emit_bit(0)
                low *= 2
                high = 2 * high + 1
            elif low >= HALF:
                emit_bit(1)
                low = 2 * (low - HALF)
                high = 2 * (high - HALF) + 1
            elif low >= QUARTER and high < 3 * QUARTER:
                pending += 1
                low = 2 * (low - QUARTER)
                high = 2 * (high - QUARTER) + 1
            else:
                break
    # Termination
    pending += 1
    if low < QUARTER:
        emit_bit(0)
    else:
        emit_bit(1)
    # Pack bits
    out = bytearray()
    for i in range(0, len(out_bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(out_bits) and out_bits[i + j]:
                byte |= 1 << (7 - j)
        out.append(byte)
    return bytes(out), freqs


def arithmetic_decode(compressed: bytes, freqs: Dict[int, int], length: int) -> bytes:
    """Decode given frequency table and original length."""
    if length == 0:
        return b""
    cum, total = _build_cum(freqs)
    # Unpack bits
    bits: List[int] = []
    for byte in compressed:
        for j in range(7, -1, -1):
            bits.append((byte >> j) & 1)
    bit_idx = 0

    def next_bit() -> int:
        nonlocal bit_idx
        if bit_idx < len(bits):
            b = bits[bit_idx]
            bit_idx += 1
            return b
        return 0

    value = 0
    for _ in range(PRECISION):
        value = 2 * value + next_bit()
    low, high = 0, FULL - 1
    result = bytearray()
    for _ in range(length):
        range_ = high - low + 1
        scaled = ((value - low + 1) * total - 1) // range_
        # Find symbol
        sym = 0
        for s in range(256):
            if cum[s + 1] > scaled:
                sym = s
                break
        result.append(sym)
        high = low + (range_ * cum[sym + 1]) // total - 1
        low = low + (range_ * cum[sym]) // total
        while True:
            if high < HALF:
                low *= 2
                high = 2 * high + 1
                value = 2 * value + next_bit()
            elif low >= HALF:
                low = 2 * (low - HALF)
                high = 2 * (high - HALF) + 1
                value = 2 * (value - HALF) + next_bit()
            elif low >= QUARTER and high < 3 * QUARTER:
                low = 2 * (low - QUARTER)
                high = 2 * (high - QUARTER) + 1
                value = 2 * (value - QUARTER) + next_bit()
            else:
                break
    return bytes(result)


if __name__ == "__main__":
    data = b"abracadabra"
    enc, freqs = arithmetic_encode(data)
    dec = arithmetic_decode(enc, freqs, len(data))
    assert dec == data
    empty, f0 = arithmetic_encode(b"")
    assert arithmetic_decode(empty, f0, 0) == b""
    data2 = bytes(range(256)) * 2
    enc2, f2 = arithmetic_encode(data2)
    assert arithmetic_decode(enc2, f2, len(data2)) == data2
    print("arithmetic_coding self-tests passed")
