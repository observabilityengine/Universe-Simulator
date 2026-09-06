"""Fermat factorization for odd integers.

Complexity: O(|a-b|) where n = a*b and a≈b; fast when factors are close.
Returns a factor pair (p, q) with p <= q, or (1, n) if prime / failure.
Original implementation.
"""
from __future__ import annotations

import math
from typing import Tuple


def fermat_factorization(n: int, max_steps: int = 1_000_000) -> Tuple[int, int]:
    """Factor n via Fermat. n should be odd and composite for best results."""
    if n < 2:
        raise ValueError("n must be >= 2")
    if n % 2 == 0:
        return (2, n // 2)
    a = math.isqrt(n) + 1
    b2 = a * a - n
    steps = 0
    while steps < max_steps:
        b = math.isqrt(b2)
        if b * b == b2:
            p, q = a - b, a + b
            return (p, q) if p <= q else (q, p)
        a += 1
        b2 = a * a - n
        steps += 1
    return (1, n)


if __name__ == "__main__":
    p, q = fermat_factorization(5959)  # 59 * 101
    assert p * q == 5959 and p > 1
    p2, q2 = fermat_factorization(15)
    assert p2 * q2 == 15
    assert fermat_factorization(17) == (1, 17)
    assert fermat_factorization(14) == (2, 7)
    try:
        fermat_factorization(1)
        assert False
    except ValueError:
        pass
    print("fermat_factorization self-tests passed")
