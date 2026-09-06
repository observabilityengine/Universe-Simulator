"""Move-to-front transform.

Complexity: O(n * σ) naïve; σ = alphabet size.
Used in compression pipelines (e.g. with BWT). Original implementation.
"""
from __future__ import annotations

from typing import List


def mtf_encode(data: bytes, alphabet: bytes | None = None) -> List[int]:
    if alphabet is None:
        alphabet = bytes(range(256))
    symbols = list(alphabet)
    out: List[int] = []
    for b in data:
        idx = symbols.index(b)
        out.append(idx)
        symbols.pop(idx)
        symbols.insert(0, b)
    return out


def mtf_decode(indices: List[int], alphabet: bytes | None = None) -> bytes:
    if alphabet is None:
        alphabet = bytes(range(256))
    symbols = list(alphabet)
    out = bytearray()
    for idx in indices:
        b = symbols[idx]
        out.append(b)
        symbols.pop(idx)
        symbols.insert(0, b)
    return bytes(out)


if __name__ == "__main__":
    data = b"abracadabra"
    enc = mtf_encode(data)
    assert mtf_decode(enc) == data
    assert mtf_decode(mtf_encode(b"")) == b""
    assert mtf_decode(mtf_encode(b"aaa")) == b"aaa"
    print("move_to_front self-tests passed")
