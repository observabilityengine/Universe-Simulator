"""Stable mergesort.

Complexity: O(n log n) time, O(n) extra space.
Stable. Works for any comparable sequence.
"""
from __future__ import annotations

from typing import List, TypeVar, Sequence

T = TypeVar("T")


def mergesort(a: Sequence[T]) -> List[T]:
    """Return a new sorted list (stable)."""
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    left = mergesort(a[:mid])
    right = mergesort(a[mid:])
    return _merge(left, right)


def _merge(left: List[T], right: List[T]) -> List[T]:
    result: List[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


if __name__ == "__main__":
    assert mergesort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]
    assert mergesort([]) == []
    assert mergesort([7]) == [7]
    assert mergesort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    assert mergesort([1, 1, 1]) == [1, 1, 1]
    data = [(1, "a"), (1, "b"), (0, "c")]
    assert mergesort(data) == [(0, "c"), (1, "a"), (1, "b")]
    print("mergesort self-tests passed")
