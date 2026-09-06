"""Bucket sort for floats in a known range.

Complexity: O(n + k) average for n elements and k buckets; O(n^2) worst.
Stable when using stable sort inside buckets. Assumes values in [min_val, max_val].
Original implementation.
"""
from __future__ import annotations

from typing import List


def bucket_sort(
    a: List[float],
    num_buckets: int | None = None,
    min_val: float | None = None,
    max_val: float | None = None,
) -> List[float]:
    """Return sorted copy of a using bucket sort."""
    if not a:
        return []
    if min_val is None:
        min_val = min(a)
    if max_val is None:
        max_val = max(a)
    if min_val == max_val:
        return list(a)
    n = len(a)
    k = num_buckets if num_buckets is not None else max(1, n)
    buckets: List[List[float]] = [[] for _ in range(k)]
    span = max_val - min_val
    for x in a:
        idx = int((x - min_val) / span * (k - 1))
        idx = max(0, min(k - 1, idx))
        buckets[idx].append(x)
    for b in buckets:
        b.sort()
    result: List[float] = []
    for b in buckets:
        result.extend(b)
    return result


if __name__ == "__main__":
    assert bucket_sort([0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]) == sorted(
        [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    )
    assert bucket_sort([]) == []
    assert bucket_sort([5.0]) == [5.0]
    assert bucket_sort([3.0, 3.0, 3.0]) == [3.0, 3.0, 3.0]
    data = [i * 0.1 for i in range(20)][::-1]
    assert bucket_sort(data) == sorted(data)
    print("bucket_sort self-tests passed")
