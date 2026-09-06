"""GCD (Euclidean) and LCM for integers.

Complexity: O(log min(a,b)).
Handles negatives and zero. Original implementation.
"""
from __future__ import annotations


def gcd(a: int, b: int) -> int:
    """Non-negative GCD."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Non-negative LCM. lcm(0,0) defined as 0."""
    if a == 0 and b == 0:
        return 0
    return abs(a // gcd(a, b) * b)


def gcd_list(values: list[int]) -> int:
    if not values:
        raise ValueError("empty")
    g = 0
    for v in values:
        g = gcd(g, v)
    return g


if __name__ == "__main__":
    assert gcd(48, 18) == 6
    assert gcd(-48, 18) == 6
    assert gcd(0, 5) == 5
    assert gcd(0, 0) == 0
    assert lcm(4, 6) == 12
    assert lcm(0, 5) == 0
    assert gcd_list([12, 18, 24]) == 6
    print("gcd_lcm self-tests passed")
