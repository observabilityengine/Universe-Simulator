"""In-place quicksort (Hoare partition).

Complexity: average O(n log n), worst O(n^2). Not stable.
Uses random pivot to mitigate worst case. Assumes comparable elements.
"""
from __future__ import annotations

import random
from typing import List, TypeVar, MutableSequence

T = TypeVar("T")


def _partition(a: MutableSequence[T], lo: int, hi: int) -> int:
    pivot_idx = random.randint(lo, hi)
    a[pivot_idx], a[hi] = a[hi], a[pivot_idx]
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i


def _qs(a: MutableSequence[T], lo: int, hi: int) -> None:
    if lo < hi:
        p = _partition(a, lo, hi)
        _qs(a, lo, p - 1)
        _qs(a, p + 1, hi)


def quicksort(a: MutableSequence[T]) -> None:
    """Sort a in-place ascending."""
    if len(a) > 1:
        _qs(a, 0, len(a) - 1)


if __name__ == "__main__":
    a = [3, 1, 4, 1, 5, 9, 2, 6]
    quicksort(a)
    assert a == sorted([3, 1, 4, 1, 5, 9, 2, 6])
    b: list[int] = []
    quicksort(b)
    assert b == []
    c = [42]
    quicksort(c)
    assert c == [42]
    d = [7] * 20
    quicksort(d)
    assert d == [7] * 20
    e = list(range(30, 0, -1))
    quicksort(e)
    assert e == list(range(1, 31))
    f = list(range(15))
    quicksort(f)
    assert f == list(range(15))
    g = [0, -1, 5, -1, 0, 3]
    quicksort(g)
    assert g == [-1, -1, 0, 0, 3, 5]
    print("quicksort self-tests passed")
