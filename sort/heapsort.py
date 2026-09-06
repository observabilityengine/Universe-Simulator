"""Heapsort (in-place).

Complexity: O(n log n). Not stable.
Uses binary max-heap.
"""
from __future__ import annotations

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def heapsort(a: MutableSequence[T]) -> None:
    """Sort a in-place ascending."""
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(a, i, n)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        _sift_down(a, 0, end)


def _sift_down(a: MutableSequence[T], start: int, end: int) -> None:
    root = start
    while True:
        child = 2 * root + 1
        if child >= end:
            break
        if child + 1 < end and a[child] < a[child + 1]:
            child += 1
        if a[root] < a[child]:
            a[root], a[child] = a[child], a[root]
            root = child
        else:
            break


if __name__ == "__main__":
    a = [3, 1, 4, 1, 5, 9, 2]
    heapsort(a)
    assert a == [1, 1, 2, 3, 4, 5, 9]
    b: list[int] = []
    heapsort(b)
    assert b == []
    c = [42]
    heapsort(c)
    assert c == [42]
    d = [5] * 10
    heapsort(d)
    assert d == [5] * 10
    e = list(range(20, 0, -1))
    heapsort(e)
    assert e == list(range(1, 21))
    print("heapsort self-tests passed")
