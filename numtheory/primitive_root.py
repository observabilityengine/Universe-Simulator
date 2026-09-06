"""Find a primitive root modulo prime p.

Complexity: O(p^{1/2} log p) typical trial.
Returns smallest primitive root of prime p, or None. Original implementation.
"""
from __future__ import annotations

import math
from typing import List, Optional


def _factors(n: int) -> List[int]:
    f = []
    x = n
    p = 2
    while p * p <= x:
        if x % p == 0:
            f.append(p)
            while x % p == 0:
                x //= p
        p += 1 if p == 2 else 2
    if x > 1:
        f.append(x)
    return f


def primitive_root(p: int) -> Optional[int]:
    """Smallest primitive root mod prime p."""
    if p == 2:
        return 1
    if p <= 1:
        raise ValueError("p must be prime >= 2")
    phi = p - 1
    factors = _factors(phi)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in factors):
            return g
    return None


if __name__ == "__main__":
    assert primitive_root(2) == 1
    assert primitive_root(3) == 2
    assert primitive_root(5) == 2
    assert primitive_root(7) == 3
    g = primitive_root(11)
    assert g is not None and pow(g, 10, 11) == 1
    print("primitive_root self-tests passed")
