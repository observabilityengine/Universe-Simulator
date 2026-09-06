"""Cocktail shaker sort (bidirectional bubble sort).

Complexity: O(n^2) worst/average, O(n) best when nearly sorted.
In-place, stable. Original implementation.
"""
from __future__ import annotations

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def cocktail_sort(a: MutableSequence[T]) -> None:
    """Sort a in-place ascending."""
    n = len(a)
    if n < 2:
        return
    left, right = 0, n - 1
    while left < right:
        swapped = False
        for i in range(left, right):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if not swapped:
            break
        right -= 1
        swapped = False
        for i in range(right, left, -1):
            if a[i - 1] > a[i]:
                a[i - 1], a[i] = a[i], a[i - 1]
                swapped = True
        if not swapped:
            break
        left += 1


if __name__ == "__main__":
    a = [5, 1, 4, 2, 8, 0, 2]
    cocktail_sort(a)
    assert a == [0, 1, 2, 2, 4, 5, 8]
    b: list[int] = []
    cocktail_sort(b)
    assert b == []
    c = [1]
    cocktail_sort(c)
    assert c == [1]
    d = list(range(15))
    cocktail_sort(d)
    assert d == list(range(15))
    e = [3, 3, 3]
    cocktail_sort(e)
    assert e == [3, 3, 3]
    print("cocktail_sort self-tests passed")
