"""Burrows-Wheeler Transform (encode / inverse).

Complexity: O(n^2 log n) naïve sort of rotations (fine for moderate n).
Original implementation.
"""
from __future__ import annotations

from typing import List, Tuple


def bwt_encode(s: str) -> Tuple[str, int]:
    """Return (L column, index of original row). Appends no sentinel; uses index."""
    if not s:
        return "", 0
    n = len(s)
    rotations = [s[i:] + s[:i] for i in range(n)]
    rotations.sort()
    primary = rotations.index(s)
    last = "".join(r[-1] for r in rotations)
    return last, primary


def bwt_decode(last: str, primary: int) -> str:
    """Inverse BWT given L column and primary index."""
    n = len(last)
    if n == 0:
        return ""
    # build first column counts
    pairs = sorted((ch, i) for i, ch in enumerate(last))
    # LF mapping: rank of each L char → position in F
    lf = [0] * n
    for rank, (_, i) in enumerate(pairs):
        lf[i] = rank
    # reconstruct by walking LF from primary
    result = [""] * n
    idx = primary
    for pos in range(n - 1, -1, -1):
        result[pos] = last[idx]
        idx = lf[idx]
    return "".join(result)


if __name__ == "__main__":
    s = "banana"
    last, idx = bwt_encode(s)
    assert bwt_decode(last, idx) == s
    assert bwt_decode(*bwt_encode("")) == ""
    assert bwt_decode(*bwt_encode("a")) == "a"
    t = "abracadabra"
    assert bwt_decode(*bwt_encode(t)) == t
    print("bwt self-tests passed")
