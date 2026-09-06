"""Odd-even (brick) sort — parallelizable bubble variant.

Complexity: O(n^2).
In-place, stable. Original implementation.
"""
from __future__ import annotations

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def odd_even_sort(a: MutableSequence[T]) -> None:
    """Sort a in-place ascending."""
    n = len(a)
    sorted_flag = False
    while not sorted_flag:
        sorted_flag = True
        for i in range(1, n - 1, 2):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                sorted_flag = False
        for i in range(0, n - 1, 2):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                sorted_flag = False


if __name__ == "__main__":
    a = [5, 3, 2, 8, 1, 4]
    odd_even_sort(a)
    assert a == [1, 2, 3, 4, 5, 8]
    b: list[int] = []
    odd_even_sort(b)
    assert b == []
    c = [1]
    odd_even_sort(c)
    assert c == [1]
    d = list(range(12, 0, -1))
    odd_even_sort(d)
    assert d == list(range(1, 13))
    print("odd_even_sort self-tests passed")
