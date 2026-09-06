"""Counting sort for integers in a known range.

Complexity: O(n + k) where k = max - min + 1.
Stable. Assumes integer keys; range must fit in memory.
"""
from __future__ import annotations

from typing import List


def counting_sort(a: List[int], min_val: int | None = None, max_val: int | None = None) -> List[int]:
    """Return sorted copy of integer list."""
    if not a:
        return []
    if min_val is None:
        min_val = min(a)
    if max_val is None:
        max_val = max(a)
    if min_val > max_val:
        raise ValueError("min_val > max_val")
    k = max_val - min_val + 1
    count = [0] * k
    for x in a:
        count[x - min_val] += 1
    for i in range(1, k):
        count[i] += count[i - 1]
    result = [0] * len(a)
    for x in reversed(a):
        idx = x - min_val
        count[idx] -= 1
        result[count[idx]] = x
    return result


if __name__ == "__main__":
    assert counting_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]
    assert counting_sort([]) == []
    assert counting_sort([7]) == [7]
    assert counting_sort([5, 5, 5]) == [5, 5, 5]
    assert counting_sort([0, -2, 3, -2, 0], -2, 3) == [-2, -2, 0, 0, 3]
    a = list(range(16)) + list(range(15, -1, -1))
    assert counting_sort(a) == sorted(a)
    print("counting_sort self-tests passed")
