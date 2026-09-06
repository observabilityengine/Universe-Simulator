"""Pancake sort via prefix reversals.

Complexity: O(n^2) flips.
In-place. Original implementation.
"""
from __future__ import annotations

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def _flip(a: MutableSequence[T], k: int) -> None:
    lo, hi = 0, k
    while lo < hi:
        a[lo], a[hi] = a[hi], a[lo]
        lo += 1
        hi -= 1


def pancake_sort(a: MutableSequence[T]) -> None:
    """Sort a in-place ascending using prefix reversals."""
    n = len(a)
    while n > 1:
        mx = max(range(n), key=lambda i: a[i])
        if mx != n - 1:
            if mx != 0:
                _flip(a, mx)
            _flip(a, n - 1)
        n -= 1


if __name__ == "__main__":
    a = [3, 1, 4, 1, 5, 9, 2]
    pancake_sort(a)
    assert a == sorted([3, 1, 4, 1, 5, 9, 2])
    b: list[int] = []
    pancake_sort(b)
    assert b == []
    c = [1]
    pancake_sort(c)
    assert c == [1]
    d = list(range(10, 0, -1))
    pancake_sort(d)
    assert d == list(range(1, 11))
    print("pancake_sort self-tests passed")
