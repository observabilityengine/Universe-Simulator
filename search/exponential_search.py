"""Exponential (galloping) search on sorted unbounded/large sequences.

Complexity: O(log i) where i is the index of the target.
Finds range via exponential probes then binary searches.
Original implementation.
"""
from __future__ import annotations

from typing import Sequence, TypeVar

T = TypeVar("T")
NOT_FOUND = -1


def exponential_search(a: Sequence[T], target: T) -> int:
    """Return index of target in sorted a, or NOT_FOUND."""
    n = len(a)
    if n == 0:
        return NOT_FOUND
    if a[0] == target:
        return 0
    bound = 1
    while bound < n and a[bound] < target:
        bound *= 2
    lo = bound // 2
    hi = min(bound, n - 1)
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
    a = list(range(0, 100, 2))
    assert exponential_search(a, 0) == 0
    assert exponential_search(a, 50) == 25
    assert exponential_search(a, 98) == 49
    assert exponential_search(a, 51) == NOT_FOUND
    assert exponential_search([], 1) == NOT_FOUND
    assert exponential_search([5], 5) == 0
    print("exponential_search self-tests passed")
