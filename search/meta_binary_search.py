"""Meta binary search (one-sided binary search).

Complexity: O(log n).
Finds largest index with a[i] <= target in sorted ascending array.
Original implementation.
"""
from __future__ import annotations

from typing import Sequence, TypeVar

T = TypeVar("T")
NOT_FOUND = -1


def meta_binary_search(a: Sequence[T], target: T) -> int:
    """Largest i with a[i] <= target, or NOT_FOUND if all greater."""
    n = len(a)
    if n == 0:
        return NOT_FOUND
    # find highest power of 2 <= n
    lg = 0
    while (1 << (lg + 1)) <= n:
        lg += 1
    pos = 0
    for i in range(lg, -1, -1):
        nxt = pos + (1 << i)
        if nxt < n and a[nxt] <= target:
            pos = nxt
    if a[pos] <= target:
        return pos
    return NOT_FOUND


if __name__ == "__main__":
    a = [1, 3, 5, 7, 9, 11]
    assert meta_binary_search(a, 7) == 3
    assert meta_binary_search(a, 1) == 0
    assert meta_binary_search(a, 11) == 5
    assert meta_binary_search(a, 0) == NOT_FOUND
    assert meta_binary_search(a, 8) == 3
    assert meta_binary_search([], 1) == NOT_FOUND
    print("meta_binary_search self-tests passed")
