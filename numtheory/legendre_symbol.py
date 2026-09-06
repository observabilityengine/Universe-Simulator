"""Legendre symbol (a/p) via Euler's criterion.

Complexity: O(log p) modular exponentiation.
p must be an odd prime. Returns 1, -1, or 0. Original implementation.
"""
from __future__ import annotations


def legendre_symbol(a: int, p: int) -> int:
    """Compute (a/p). p odd prime assumed."""
    if p <= 2 or p % 2 == 0:
        raise ValueError("p must be an odd prime")
    a %= p
    if a == 0:
        return 0
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


if __name__ == "__main__":
    assert legendre_symbol(2, 7) == 1
    assert legendre_symbol(3, 7) == -1
    assert legendre_symbol(0, 7) == 0
    assert legendre_symbol(1, 5) == 1
    assert legendre_symbol(2, 5) == -1
    try:
        legendre_symbol(1, 2)
        assert False
    except ValueError:
        pass
    print("legendre_symbol self-tests passed")
