"""Extended Euclidean algorithm.

Complexity: O(log min(a,b)). Original implementation.
"""
from __future__ import annotations
from typing import Tuple

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Return (g, x, y) such that a*x + b*y = g = gcd(a,b)."""
    if b == 0:
        return abs(a), (1 if a >= 0 else -1), 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def modinv(a: int, m: int) -> int:
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("inverse does not exist")
    return x % m

if __name__ == "__main__":
    g, x, y = extended_gcd(240, 46)
    assert g == 2
    assert 240*x + 46*y == 2
    assert modinv(3, 11) == 4
    print("extended_gcd self-tests passed")
