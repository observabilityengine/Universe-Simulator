"""Sieve of Eratosthenes for primes up to n.

Complexity: O(n log log n) time, O(n) space.
Assumes n fits in memory; n >= 0.
"""
from __future__ import annotations

from typing import List


def sieve_eratosthenes(n: int) -> List[int]:
    """Return list of all primes <= n."""
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i, p in enumerate(is_prime) if p]


if __name__ == "__main__":
    assert sieve_eratosthenes(1) == []
    assert sieve_eratosthenes(0) == []
    assert sieve_eratosthenes(2) == [2]
    assert sieve_eratosthenes(10) == [2, 3, 5, 7]
    assert sieve_eratosthenes(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    p = sieve_eratosthenes(32)
    assert 31 in p and 32 not in p
    print("sieve_eratosthenes self-tests passed")
