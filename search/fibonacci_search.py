"""Fibonacci search on sorted sequence.

Complexity: O(log n).
Returns index or -1. Assumes ascending sorted sequence.
Original implementation.
"""
from __future__ import annotations

from typing import Sequence, TypeVar

T = TypeVar("T")
NOT_FOUND = -1


def fibonacci_search(a: Sequence[T], target: T) -> int:
    """Return index of target in sorted a, or NOT_FOUND."""
    n = len(a)
    if n == 0:
        return NOT_FOUND
    fib2, fib1 = 0, 1  # F(k-2), F(k-1)
    fib = fib1 + fib2
    while fib < n:
        fib2, fib1 = fib1, fib
        fib = fib1 + fib2
    offset = -1
    while fib > 1:
        i = min(offset + fib2, n - 1)
        if a[i] < target:
            fib, fib1, fib2 = fib1, fib2, fib1 - fib2
            offset = i
        elif a[i] > target:
            fib, fib1, fib2 = fib2, fib1 - fib2, fib2 - (fib1 - fib2)
        else:
            return i
    if fib1 and offset + 1 < n and a[offset + 1] == target:
        return offset + 1
    return NOT_FOUND


if __name__ == "__main__":
    a = [10, 22, 35, 40, 45, 50, 80, 82, 85, 90, 100]
    assert fibonacci_search(a, 85) == 8
    assert fibonacci_search(a, 10) == 0
    assert fibonacci_search(a, 100) == 10
    assert fibonacci_search(a, 99) == NOT_FOUND
    assert fibonacci_search([], 1) == NOT_FOUND
    assert fibonacci_search([5], 5) == 0
    print("fibonacci_search self-tests passed")
