"""Simplified TimSort: run detection + merge of natural runs.

Complexity: O(n log n) worst; O(n) on already-sorted.
Stable. Original educational implementation (not CPython's full TimSort).
"""
from __future__ import annotations

from typing import List, MutableSequence, TypeVar

T = TypeVar("T")


def _merge(left: List[T], right: List[T]) -> List[T]:
    result: List[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def tim_sort_simplified(a: MutableSequence[T]) -> None:
    """Sort a in-place using natural-run merge."""
    n = len(a)
    if n < 2:
        return
    runs: List[List[T]] = []
    i = 0
    while i < n:
        j = i + 1
        if j < n and a[j] < a[i]:
            while j < n and a[j] < a[j - 1]:
                j += 1
            run = list(reversed(a[i:j]))
        else:
            while j < n and a[j] >= a[j - 1]:
                j += 1
            run = list(a[i:j])
        runs.append(run)
        i = j
    while len(runs) > 1:
        new_runs: List[List[T]] = []
        for k in range(0, len(runs), 2):
            if k + 1 < len(runs):
                new_runs.append(_merge(runs[k], runs[k + 1]))
            else:
                new_runs.append(runs[k])
        runs = new_runs
    sorted_a = runs[0]
    for i, v in enumerate(sorted_a):
        a[i] = v


if __name__ == "__main__":
    a = [5, 4, 3, 2, 1, 6, 7, 8]
    tim_sort_simplified(a)
    assert a == [1, 2, 3, 4, 5, 6, 7, 8]
    b = list(range(20))
    tim_sort_simplified(b)
    assert b == list(range(20))
    c: list[int] = []
    tim_sort_simplified(c)
    assert c == []
    d = [3, 1, 2]
    tim_sort_simplified(d)
    assert d == [1, 2, 3]
    print("tim_sort_simplified self-tests passed")
