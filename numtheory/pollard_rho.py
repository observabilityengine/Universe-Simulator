"""Pollard's Rho integer factorization.

Complexity: expected O(n^{1/4}).
Finds a non-trivial factor of composite n. Returns n itself if prime or failure after attempts.
Assumes n > 1.
"""
from __future__ import annotations

import random
import math


def pollard_rho(n: int, max_attempts: int = 20) -> int:
    """Return a non-trivial factor of n, or n if none found / prime."""
    if n <= 1:
        raise ValueError("n must be > 1")
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    for _ in range(max_attempts):
        c = random.randrange(1, n)
        x = random.randrange(0, n)
        y = x
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
            if d == n:
                break
        if 1 < d < n:
            return d
    return n


if __name__ == "__main__":
    f = pollard_rho(8051)
    assert f in (83, 97)
    assert pollard_rho(17) == 17
    assert pollard_rho(100) in (2, 4, 5, 10, 20, 25, 50)
    assert pollard_rho(2) == 2
    try:
        pollard_rho(1)
        assert False
    except ValueError:
        pass
    n = 104729 * 104723
    f = pollard_rho(n)
    assert 1 < f < n and n % f == 0
    print("pollard_rho self-tests passed")
