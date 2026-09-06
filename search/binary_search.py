"""Binary search on sorted sequence.

Complexity: O(log n).
Returns index of target or -1 if not found (sentinel safe because indices >=0).
Assumes ascending sorted sequence.
"""
from __future__ import annotations

from typing import Sequence, TypeVar

T = TypeVar("T")

NOT_FOUND = -1


def binary_search(a: Sequence[T], target: T) -> int:
    """Return index of target in sorted a, or NOT_FOUND."""
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return NOT_FOUND


if __name__ == "__main__":
    a = [1, 3, 5, 7, 9]
    assert binary_search(a, 5) == 2
    assert binary_search(a, 1) == 0
    assert binary_search(a, 9) == 4
    assert binary_search(a, 4) == NOT_FOUND
    assert binary_search([], 1) == NOT_FOUND
    assert binary_search([42], 42) == 0
    assert binary_search([42], 0) == NOT_FOUND
    b = [7] * 10
    idx = binary_search(b, 7)
    assert 0 <= idx < 10
    assert binary_search(b, 6) == NOT_FOUND
    print("binary_search self-tests passed")
