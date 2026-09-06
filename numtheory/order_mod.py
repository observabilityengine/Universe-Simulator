"""Multiplicative order of a modulo n.

Complexity: O(sqrt(φ(n)) log n) factoring + checks.
Smallest k > 0 with a^k ≡ 1 (mod n). Original implementation.
"""
from __future__ import annotations

import math
from typing import Optional


def order_mod(a: int, n: int) -> Optional[int]:
    """Multiplicative order of a mod n, or None if gcd(a,n) != 1."""
    if n <= 1:
        raise ValueError("n must be > 1")
    a %= n
    if math.gcd(a, n) != 1:
        return None
    # order divides φ(n); compute φ via factorization of n
    phi = n
    x = n
    p = 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            phi -= phi // p
        p += 1 if p == 2 else 2
    if x > 1:
        phi -= phi // x
    # find smallest k | phi with a^k ≡ 1
    # factor phi
    factors = []
    t = phi
    p = 2
    while p * p <= t:
        if t % p == 0:
            factors.append(p)
            while t % p == 0:
                t //= p
        p += 1 if p == 2 else 2
    if t > 1:
        factors.append(t)
    order = phi
    for q in factors:
        while order % q == 0 and pow(a, order // q, n) == 1:
            order //= q
    return order


if __name__ == "__main__":
    assert order_mod(2, 7) == 3
    assert order_mod(3, 7) == 6
    assert order_mod(2, 5) == 4
    assert order_mod(2, 4) is None
    print("order_mod self-tests passed")
