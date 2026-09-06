"""Ubiquitous binary search variants: lower_bound and upper_bound.

Complexity: O(log n).
lower_bound: first index with a[i] >= target
upper_bound: first index with a[i] > target
Assumes ascending sorted sequence. Original implementation.
"""
from __future__ import annotations

from typing import Sequence, TypeVar

T = TypeVar("T")


def lower_bound(a: Sequence[T], target: T) -> int:
    """First index i where a[i] >= target, or len(a)."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(a: Sequence[T], target: T) -> int:
    """First index i where a[i] > target, or len(a)."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


if __name__ == "__main__":
    a = [1, 2, 2, 2, 3, 5]
    assert lower_bound(a, 2) == 1
    assert upper_bound(a, 2) == 4
    assert lower_bound(a, 4) == 5
    assert upper_bound(a, 5) == 6
    assert lower_bound(a, 0) == 0
    assert lower_bound([], 1) == 0
    assert lower_bound([1, 3, 5], 3) == 1
    print("ubiquitous_binary_search self-tests passed")
