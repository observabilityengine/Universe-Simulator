"""Baby-step giant-step discrete logarithm.

Complexity: O(sqrt(m)) time and space for modulus m.
Solves g^x ≡ h (mod p) for prime p (or order of g).
Returns x in [0, order) or None if no solution.
Original implementation.
"""
from __future__ import annotations

import math
from typing import Dict, Optional


def babystep_giantstep(g: int, h: int, p: int) -> Optional[int]:
    """Find x such that pow(g, x, p) == h % p. Assumes p prime, g generator or order divides p-1."""
    if p <= 1:
        raise ValueError("p must be > 1")
    g %= p
    h %= p
    if h == 1:
        return 0
    if g == 0:
        return 0 if h == 0 else None
    m = int(math.ceil(math.sqrt(p - 1)))
    table: Dict[int, int] = {}
    e = 1
    for j in range(m):
        if e not in table:
            table[e] = j
        e = (e * g) % p
    # factor = g^{-m} mod p
    inv_g_m = pow(g, p - 1 - m, p)  # g^{-m} via Fermat when p prime
    gamma = h
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = (gamma * inv_g_m) % p
    return None


if __name__ == "__main__":
    # 2^x ≡ 22 (mod 29) → x = 17? check
    x = babystep_giantstep(2, 22, 29)
    assert x is not None and pow(2, x, 29) == 22
    assert babystep_giantstep(2, 1, 29) == 0
    assert babystep_giantstep(3, 13, 17) is not None
    assert pow(3, babystep_giantstep(3, 13, 17), 17) == 13
    try:
        babystep_giantstep(2, 1, 1)
        assert False
    except ValueError:
        pass
    print("babystep_giantstep self-tests passed")
