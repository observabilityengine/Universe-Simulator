"""General Chinese Remainder Theorem for non-pairwise-coprime moduli.

Complexity: O(k log M) for k congruences.
Solves x ≡ a_i (mod m_i). Returns (x, lcm) or raises if inconsistent.
Original implementation (extends basic CRT).
"""
from __future__ import annotations

import math
from typing import List, Tuple


def crt_general(congruences: List[Tuple[int, int]]) -> Tuple[int, int]:
    """Solve system x ≡ a_i (mod m_i). Returns (x0, mod) with x0 in [0, mod).

    Raises ValueError if no solution.
    """
    if not congruences:
        raise ValueError("empty system")
    x, m = congruences[0]
    x %= m
    for a, mi in congruences[1:]:
        a %= mi
        g = math.gcd(m, mi)
        if (a - x) % g != 0:
            raise ValueError("no solution: incongruent system")
        # solve m * t ≡ (a - x) (mod mi)  →  (m/g)*t ≡ ((a-x)/g) (mod mi/g)
        m1, m2 = m // g, mi // g
        inv = pow(m1, -1, m2)
        t = ((a - x) // g * inv) % m2
        x = x + m * t
        m = m * m2
        x %= m
    return x, m


if __name__ == "__main__":
    x, mod = crt_general([(2, 3), (3, 5), (2, 7)])
    assert x % 3 == 2 and x % 5 == 3 and x % 7 == 2
    assert mod == 105
    x2, m2 = crt_general([(0, 2), (0, 4)])  # consistent non-coprime
    assert x2 % 2 == 0 and x2 % 4 == 0
    try:
        crt_general([(1, 2), (2, 4)])  # inconsistent
        assert False
    except ValueError:
        pass
    try:
        crt_general([])
        assert False
    except ValueError:
        pass
    print("chinese_remainder_general self-tests passed")
