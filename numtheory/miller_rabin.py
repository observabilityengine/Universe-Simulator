"""Miller-Rabin primality test.

Complexity: O(k log^3 n) with k witnesses. Original implementation.
"""
from __future__ import annotations

import random
from typing import List


def _powmod(base: int, exp: int, mod: int) -> int:
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result


def is_prime(n: int, k: int = 12, seed: int = 42) -> bool:
    """Miller-Rabin probabilistic primality test."""
    if n < 2:
        return False
    if n in (2, 3, 5, 7):
        return True
    if n % 2 == 0 or n % 3 == 0 or n % 5 == 0 or n % 7 == 0:
        return False

    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    rng = random.Random(seed)
    bases = [2, 3, 5, 7, 11, 13, 23]
    while len(bases) < k:
        a = rng.randrange(2, n - 1)
        if a not in bases:
            bases.append(a)

    for a in bases:
        if a >= n:
            continue
        x = _powmod(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for _ in range(s - 1):
            x = _powmod(x, 2, n)
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True


if __name__ == "__main__":
    assert is_prime(2)
    assert is_prime(3)
    assert is_prime(97)
    assert is_prime(10**9 + 7)
    assert not is_prime(1)
    assert not is_prime(91)
    assert not is_prime(100)
    assert not is_prime(2047)
    assert is_prime(32416190071)
    print("miller_rabin self-tests passed")
