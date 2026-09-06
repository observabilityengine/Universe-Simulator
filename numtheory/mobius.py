"""Möbius function μ(n).

Complexity: O(sqrt(n)) per evaluation; sieve for range.
μ(n) = 0 if square factor; else (-1)^k for k distinct prime factors.
Original implementation.
"""
from __future__ import annotations

from typing import List


def mobius(n: int) -> int:
    if n < 1:
        raise ValueError("n must be >= 1")
    if n == 1:
        return 1
    result = 1
    x = n
    p = 2
    while p * p <= x:
        if x % p == 0:
            x //= p
            if x % p == 0:
                return 0
            result = -result
        p += 1 if p == 2 else 2
    if x > 1:
        result = -result
    return result


def mobius_sieve(n: int) -> List[int]:
    """μ(0..n); μ[0] unused (=0)."""
    if n < 0:
        raise ValueError("n >= 0")
    mu = [1] * (n + 1)
    prime = [True] * (n + 1)
    if n >= 0:
        mu[0] = 0
    for i in range(2, n + 1):
        if prime[i]:
            for j in range(i, n + 1, i):
                prime[j] = False if j != i else prime[j]
                mu[j] = -mu[j]
            sq = i * i
            for j in range(sq, n + 1, sq):
                mu[j] = 0
    return mu


if __name__ == "__main__":
    assert mobius(1) == 1
    assert mobius(2) == -1
    assert mobius(6) == 1
    assert mobius(4) == 0
    assert mobius(30) == -1
    sieve = mobius_sieve(10)
    for i in range(1, 11):
        assert sieve[i] == mobius(i)
    print("mobius self-tests passed")
