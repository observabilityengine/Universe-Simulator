"""Selection sort.

Complexity: O(n^2) comparisons always.
In-place, not stable. Original implementation.
"""
from __future__ import annotations

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def selection_sort(a: MutableSequence[T]) -> None:
    """Sort a in-place ascending."""
    n = len(a)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]


if __name__ == "__main__":
    a = [64, 25, 12, 22, 11]
    selection_sort(a)
    assert a == [11, 12, 22, 25, 64]
    b: list[int] = []
    selection_sort(b)
    assert b == []
    c = [1]
    selection_sort(c)
    assert c == [1]
    d = list(range(15))
    selection_sort(d)
    assert d == list(range(15))
    print("selection_sort self-tests passed")
