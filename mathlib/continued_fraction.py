"""Continued fraction expansion of a rational / float.

Complexity: O(steps).
Returns list of partial quotients [a0; a1, a2, ...]. Original implementation.
"""
from __future__ import annotations

from typing import List, Tuple


def continued_fraction_rational(num: int, den: int) -> List[int]:
    """CF expansion of num/den."""
    if den == 0:
        raise ValueError("denominator zero")
    result: List[int] = []
    while den:
        q = num // den
        result.append(q)
        num, den = den, num - q * den
    return result


def continued_fraction_float(x: float, max_terms: int = 30, tol: float = 1e-12) -> List[int]:
    """CF expansion of a float."""
    result: List[int] = []
    for _ in range(max_terms):
        a = int(x)
        result.append(a)
        frac = x - a
        if abs(frac) < tol:
            break
        x = 1.0 / frac
    return result


def cf_convergent(coeffs: List[int]) -> Tuple[int, int]:
    """Return (num, den) convergent of CF coefficients."""
    if not coeffs:
        return 0, 1
    n0, d0 = coeffs[0], 1
    if len(coeffs) == 1:
        return n0, d0
    n1, d1 = coeffs[0] * coeffs[1] + 1, coeffs[1]
    for a in coeffs[2:]:
        n0, n1 = n1, a * n1 + n0
        d0, d1 = d1, a * d1 + d0
    return n1, d1


if __name__ == "__main__":
    assert continued_fraction_rational(13, 11) == [1, 5, 2]
    n, d = cf_convergent([1, 5, 2])
    assert n == 13 and d == 11
    cf = continued_fraction_float(3.14159, max_terms=10)
    assert cf[0] == 3
    print("continued_fraction self-tests passed")
