"""Comb sort — improved bubble sort with shrinking gap.

Complexity: average ~O(n^2 / 2^p); shrink factor 1.3 is standard.
In-place, not stable. Original implementation.
"""
from __future__ import annotations

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def comb_sort(a: MutableSequence[T]) -> None:
    """Sort a in-place ascending."""
    n = len(a)
    gap = n
    shrink = 1.3
    sorted_flag = False
    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        i = 0
        while i + gap < n:
            if a[i] > a[i + gap]:
                a[i], a[i + gap] = a[i + gap], a[i]
                sorted_flag = False
            i += 1


if __name__ == "__main__":
    a = [8, 4, 1, 56, 3, -44, 23, -6, 28, 0]
    comb_sort(a)
    assert a == sorted([8, 4, 1, 56, 3, -44, 23, -6, 28, 0])
    b: list[int] = []
    comb_sort(b)
    assert b == []
    c = [1]
    comb_sort(c)
    assert c == [1]
    d = list(range(30, 0, -1))
    comb_sort(d)
    assert d == list(range(1, 31))
    print("comb_sort self-tests passed")
