"""Cycle sort — minimizes writes to memory.

Complexity: O(n^2) comparisons; at most n writes.
In-place, not stable. Original implementation.
"""
from __future__ import annotations

from typing import MutableSequence, TypeVar

T = TypeVar("T")


def cycle_sort(a: MutableSequence[T]) -> int:
    """Sort a in-place; returns number of writes performed."""
    writes = 0
    n = len(a)
    for cycle_start in range(n - 1):
        item = a[cycle_start]
        pos = cycle_start
        for i in range(cycle_start + 1, n):
            if a[i] < item:
                pos += 1
        if pos == cycle_start:
            continue
        while item == a[pos]:
            pos += 1
        a[pos], item = item, a[pos]
        writes += 1
        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                if a[i] < item:
                    pos += 1
            while item == a[pos]:
                pos += 1
            a[pos], item = item, a[pos]
            writes += 1
    return writes


if __name__ == "__main__":
    a = [5, 2, 4, 1, 3]
    w = cycle_sort(a)
    assert a == [1, 2, 3, 4, 5]
    assert w >= 0
    b: list[int] = []
    assert cycle_sort(b) == 0
    c = [2, 2, 2]
    cycle_sort(c)
    assert c == [2, 2, 2]
    print("cycle_sort self-tests passed")
