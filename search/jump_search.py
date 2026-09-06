"""Jump search on sorted sequence.

Complexity: O(sqrt(n)).
Returns index of target or -1. Assumes ascending sorted sequence.
Original implementation.
"""
from __future__ import annotations

import math
from typing import Sequence, TypeVar

T = TypeVar("T")
NOT_FOUND = -1


def jump_search(a: Sequence[T], target: T) -> int:
    """Return index of target in sorted a, or NOT_FOUND."""
    n = len(a)
    if n == 0:
        return NOT_FOUND
    step = int(math.sqrt(n))
    prev = 0
    while prev < n and a[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return NOT_FOUND
    for i in range(prev, min(step, n)):
        if a[i] == target:
            return i
    return NOT_FOUND


if __name__ == "__main__":
    a = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
    assert jump_search(a, 55) == 10
    assert jump_search(a, 0) == 0
    assert jump_search(a, 144) == 12
    assert jump_search(a, 4) == NOT_FOUND
    assert jump_search([], 1) == NOT_FOUND
    assert jump_search([7], 7) == 0
    assert jump_search([7], 0) == NOT_FOUND
    print("jump_search self-tests passed")
