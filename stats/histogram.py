"""Histogram construction for 1-D numeric data.

Complexity: O(n + k) for n samples and k bins.
Supports fixed bin count or explicit edges. Original implementation.
"""
from __future__ import annotations

from typing import List, Sequence, Tuple


def histogram(
    data: Sequence[float],
    bins: int | Sequence[float] = 10,
) -> Tuple[List[int], List[float]]:
    """Return (counts, edges). edges has length len(counts)+1."""
    if not data:
        if isinstance(bins, int):
            return [0] * bins, [0.0] * (bins + 1)
        edges = list(bins)
        return [0] * (len(edges) - 1), edges
    if isinstance(bins, int):
        if bins < 1:
            raise ValueError("bins must be >= 1")
        lo, hi = min(data), max(data)
        if lo == hi:
            hi = lo + 1.0
        edges = [lo + i * (hi - lo) / bins for i in range(bins + 1)]
        edges[-1] = hi  # ensure last edge exact
    else:
        edges = list(bins)
        if len(edges) < 2:
            raise ValueError("need at least 2 edges")
    k = len(edges) - 1
    counts = [0] * k
    for x in data:
        if x < edges[0] or x > edges[-1]:
            continue
        # rightmost bin includes upper edge
        if x == edges[-1]:
            counts[-1] += 1
            continue
        # binary search style
        lo, hi = 0, k - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if edges[mid] <= x < edges[mid + 1]:
                counts[mid] += 1
                break
            if x < edges[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
    return counts, edges


if __name__ == "__main__":
    counts, edges = histogram([1, 2, 2, 3, 4], bins=4)
    assert sum(counts) == 5
    assert len(edges) == 5
    c2, e2 = histogram([5.0, 5.0, 5.0], bins=3)
    assert sum(c2) == 3
    c3, _ = histogram([], bins=5)
    assert c3 == [0, 0, 0, 0, 0]
    c4, e4 = histogram([0.5, 1.5, 2.5], bins=[0, 1, 2, 3])
    assert c4 == [1, 1, 1]
    print("histogram self-tests passed")
