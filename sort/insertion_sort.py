"""Insertion sort.

Complexity: O(n^2) worst/average, O(n) best (already sorted).
In-place, stable. Original implementation.
"""
from __future__ import annotations

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def insertion_sort(a: MutableSequence[T]) -> None:
    """Sort a in-place ascending."""
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key


if __name__ == "__main__":
    a = [5, 2, 4, 6, 1, 3]
    insertion_sort(a)
    assert a == [1, 2, 3, 4, 5, 6]
    b: list[int] = []
    insertion_sort(b)
    assert b == []
    c = [1]
    insertion_sort(c)
    assert c == [1]
    d = [3, 3, 3]
    insertion_sort(d)
    assert d == [3, 3, 3]
    e = list(range(20, 0, -1))
    insertion_sort(e)
    assert e == list(range(1, 21))
    print("insertion_sort self-tests passed")
