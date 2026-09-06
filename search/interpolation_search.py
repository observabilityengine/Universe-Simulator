"""Interpolation search on sorted uniformly distributed numeric sequences.

Complexity: average O(log log n) for uniform data; O(n) worst case.
Returns index or -1. Assumes ascending sorted sequence of numbers.
Original implementation.
"""
from __future__ import annotations

from typing import Sequence

NOT_FOUND = -1


def interpolation_search(a: Sequence[float], target: float) -> int:
    """Return index of target in sorted a, or NOT_FOUND."""
    lo, hi = 0, len(a) - 1
    while lo <= hi and a[lo] <= target <= a[hi]:
        if lo == hi:
            return lo if a[lo] == target else NOT_FOUND
        denom = a[hi] - a[lo]
        if denom == 0:
            return lo if a[lo] == target else NOT_FOUND
        pos = lo + int((hi - lo) * (target - a[lo]) / denom)
        pos = max(lo, min(hi, pos))
        if a[pos] == target:
            return pos
        if a[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return NOT_FOUND


if __name__ == "__main__":
    a = [10, 12, 13, 16, 18, 19, 20, 21, 22, 23, 24, 33, 35, 42, 47]
    assert interpolation_search(a, 18) == 4
    assert interpolation_search(a, 10) == 0
    assert interpolation_search(a, 47) == 14
    assert interpolation_search(a, 15) == NOT_FOUND
    assert interpolation_search([], 1) == NOT_FOUND
    assert interpolation_search([5], 5) == 0
    assert interpolation_search([5], 3) == NOT_FOUND
    assert interpolation_search([2, 2, 2], 2) in (0, 1, 2)
    print("interpolation_search self-tests passed")
