"""Pollard's Rho integer factorization.

Complexity: O(n^{1/4}) expected. Original implementation.
"""
from __future__ import annotations
import random
from typing import List, Optional

def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)

def pollard_rho(n: int, seed: int = 42, max_attempts: int = 20) -> Optional[int]:
    if n < 2:
        return None
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    rng = random.Random(seed)
    for attempt in range(max_attempts):
        c = rng.randrange(1, n)
        x = rng.randrange(0, n)
        y = x
        d = 1
        f = lambda v: (v * v + c) % n
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = _gcd(abs(x - y), n)
        if d != n:
            return d
    return None

def factorize(n: int, seed: int = 42) -> List[int]:
    if n < 2:
        return []
    factors: List[int] = []
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        while n % p == 0:
            factors.append(p)
            n //= p
    if n == 1:
        return sorted(factors)

    def _is_prime_simple(x: int) -> bool:
        if x < 2: return False
        if x < 4: return True
        if x % 2 == 0 or x % 3 == 0: return False
        i = 5
        while i * i <= x:
            if x % i == 0 or x % (i + 2) == 0: return False
            i += 6
        return True

    def _factor(m: int, s: int) -> None:
        if m == 1: return
        if _is_prime_simple(m):
            factors.append(m)
            return
        d = pollard_rho(m, seed=s)
        if d is None or d == m:
            factors.append(m)
            return
        _factor(d, s + 1)
        _factor(m // d, s + 2)

    _factor(n, seed)
    return sorted(factors)

if __name__ == "__main__":
    assert pollard_rho(15) in (3, 5)
    assert pollard_rho(91) in (7, 13)
    assert factorize(12) == [2, 2, 3]
    assert factorize(97) == [97]
    assert sorted(factorize(1001)) == [7, 11, 13]
    print("pollard_rho self-tests passed")
