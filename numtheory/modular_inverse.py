"""Modular multiplicative inverse via extended Euclid.

Complexity: O(log m).
Returns inverse of a mod m if gcd(a, m) == 1, else raises ValueError.
m > 1 assumed; a may be any int.
"""
from __future__ import annotations

from .extended_gcd import extended_gcd


def modular_inverse(a: int, m: int) -> int:
    """Return x such that (a * x) % m == 1."""
    if m <= 1:
        raise ValueError("modulus must be > 1")
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError("inverse does not exist")
    return x % m


if __name__ == "__main__":
    assert modular_inverse(3, 11) == 4
    assert modular_inverse(10, 17) == 12
    assert (7 * modular_inverse(7, 13)) % 13 == 1
    try:
        modular_inverse(2, 4)
        assert False
    except ValueError:
        pass
    try:
        modular_inverse(1, 1)
        assert False
    except ValueError:
        pass
    inv = modular_inverse(-3, 11)
    assert ((-3) * inv) % 11 == 1
    print("modular_inverse self-tests passed")
