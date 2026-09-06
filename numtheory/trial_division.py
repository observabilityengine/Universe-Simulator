"""Trial division factorization and primality.

Complexity: O(sqrt(n)) for factoring / primality of n.
Returns sorted list of prime factors with multiplicity.
Original implementation.
"""
from __future__ import annotations

from typing import List


def is_prime(n: int) -> bool:
    """Deterministic trial-division primality test."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def trial_division(n: int) -> List[int]:
    """Return prime factors of n in ascending order (with multiplicity)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return []
    factors: List[int] = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    while n % 3 == 0:
        factors.append(3)
        n //= 3
    i = 5
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        while n % (i + 2) == 0:
            factors.append(i + 2)
            n //= i + 2
        i += 6
    if n > 1:
        factors.append(n)
    return factors


if __name__ == "__main__":
    assert trial_division(1) == []
    assert trial_division(0) == []
    assert trial_division(2) == [2]
    assert trial_division(12) == [2, 2, 3]
    assert trial_division(97) == [97]
    assert trial_division(100) == [2, 2, 5, 5]
    assert is_prime(2) and is_prime(97) and not is_prime(1) and not is_prime(100)
    prod = 1
    for f in trial_division(840):
        prod *= f
    assert prod == 840
    print("trial_division self-tests passed")
