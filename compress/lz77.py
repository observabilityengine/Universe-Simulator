"""
Universe Simulator - LZ77 Compression (simple window)
Original sliding-window encode / decode.
"""

from __future__ import annotations

from typing import List, Tuple

Token = Tuple[int, int, int]  # (offset, length, next_byte)


def lz77_encode(data: bytes, window: int = 32) -> List[Token]:
    i = 0
    n = len(data)
    out: List[Token] = []
    while i < n:
        best_off = 0
        best_len = 0
        start = max(0, i - window)
        for j in range(start, i):
            length = 0
            while i + length < n and data[j + length] == data[i + length] and length < 255:
                length += 1
                if j + length >= i:
                    break
            if length > best_len:
                best_len = length
                best_off = i - j
        next_byte = data[i + best_len] if i + best_len < n else 0
        out.append((best_off, best_len, next_byte))
        i += best_len + 1
    return out


def lz77_decode(tokens: List[Token]) -> bytes:
    out = bytearray()
    for off, length, nxt in tokens:
        if length > 0:
            start = len(out) - off
            for k in range(length):
                out.append(out[start + k])
        if nxt or length == 0:
            out.append(nxt)
    return bytes(out)


if __name__ == "__main__":
    original = b"abracadabra"
    enc = lz77_encode(original)
    dec = lz77_decode(enc)
    assert dec == original
    print("lz77 self-test passed", enc)
