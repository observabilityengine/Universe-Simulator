"""Sieve of Eratosthenes and segmented variant.

Complexity: O(n log log n). Original implementation.
"""
from __future__ import annotations

from typing import List
import math


def sieve(n: int) -> List[int]:
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]


def segmented_sieve(L: int, R: int) -> List[int]:
    if R < 2:
        return []
    L = max(L, 2)
    limit = int(math.sqrt(R)) + 1
    base = sieve(limit)
    is_prime = [True] * (R - L + 1)
    for p in base:
        start = max(p * p, ((L + p - 1) // p) * p)
        for j in range(start, R + 1, p):
            is_prime[j - L] = False
    return [L + i for i in range(R - L + 1) if is_prime[i]]


if __name__ == "__main__":
    assert sieve(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert sieve(1) == []
    assert segmented_sieve(10, 30) == [11, 13, 17, 19, 23, 29]
    print("sieve self-tests passed")
