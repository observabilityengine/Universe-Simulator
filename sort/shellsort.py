"""Shell sort (diminishing gap insertion sort).

Complexity: depends on gap sequence; with Hibbard gaps O(n^{1.5}) worst-case typical.
In-place, not stable. Original implementation.
"""
from __future__ import annotations

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def shellsort(a: MutableSequence[T]) -> None:
    """Sort a in-place ascending using Shell sort with Hibbard gaps."""
    n = len(a)
    gap = 1
    while gap < n // 3:
        gap = 3 * gap + 1
    while gap >= 1:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
        gap //= 3


if __name__ == "__main__":
    a = [9, 8, 3, 7, 5, 6, 4, 1]
    shellsort(a)
    assert a == sorted([9, 8, 3, 7, 5, 6, 4, 1])
    b: list[int] = []
    shellsort(b)
    assert b == []
    c = [42]
    shellsort(c)
    assert c == [42]
    d = [5] * 12
    shellsort(d)
    assert d == [5] * 12
    e = list(range(25, 0, -1))
    shellsort(e)
    assert e == list(range(1, 26))
    print("shellsort self-tests passed")
