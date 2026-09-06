"""Gnome sort (stupid sort).

Complexity: O(n^2) worst, O(n) best.
In-place, stable. Original implementation.
"""
from __future__ import annotations

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def gnome_sort(a: MutableSequence[T]) -> None:
    """Sort a in-place ascending."""
    i = 0
    n = len(a)
    while i < n:
        if i == 0 or a[i] >= a[i - 1]:
            i += 1
        else:
            a[i], a[i - 1] = a[i - 1], a[i]
            i -= 1


if __name__ == "__main__":
    a = [34, 2, 10, -9]
    gnome_sort(a)
    assert a == [-9, 2, 10, 34]
    b: list[int] = []
    gnome_sort(b)
    assert b == []
    c = [1, 1, 1]
    gnome_sort(c)
    assert c == [1, 1, 1]
    d = list(range(12, 0, -1))
    gnome_sort(d)
    assert d == list(range(1, 13))
    print("gnome_sort self-tests passed")
