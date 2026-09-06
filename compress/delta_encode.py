"""Delta encoding / decoding for integer sequences.

Complexity: O(n).
Stores first value then successive differences — effective for smooth series.
Original implementation.
"""
from __future__ import annotations

from typing import List


def delta_encode(data: List[int]) -> List[int]:
    """Encode as [x0, x1-x0, x2-x1, ...]."""
    if not data:
        return []
    out = [data[0]]
    for i in range(1, len(data)):
        out.append(data[i] - data[i - 1])
    return out


def delta_decode(encoded: List[int]) -> List[int]:
    """Inverse of delta_encode."""
    if not encoded:
        return []
    out = [encoded[0]]
    for i in range(1, len(encoded)):
        out.append(out[-1] + encoded[i])
    return out


if __name__ == "__main__":
    data = [100, 105, 107, 110, 108]
    enc = delta_encode(data)
    assert enc == [100, 5, 2, 3, -2]
    assert delta_decode(enc) == data
    assert delta_decode(delta_encode([])) == []
    assert delta_decode(delta_encode([42])) == [42]
    seq = list(range(1000))
    assert delta_decode(delta_encode(seq)) == seq
    print("delta_encode self-tests passed")
