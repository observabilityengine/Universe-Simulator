"""Euler's totient φ(n) via prime factorization.

Complexity: O(sqrt(n)).
Returns number of integers in 1..n coprime to n. Original implementation.
"""
from __future__ import annotations


def euler_totient(n: int) -> int:
    """Return φ(n)."""
    if n < 1:
        raise ValueError("n must be >= 1")
    result = n
    p = 2
    x = n
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            result -= result // p
        p += 1 if p == 2 else 2
    if x > 1:
        result -= result // x
    return result


if __name__ == "__main__":
    assert euler_totient(1) == 1
    assert euler_totient(2) == 1
    assert euler_totient(9) == 6
    assert euler_totient(10) == 4
    assert euler_totient(7) == 6
    assert euler_totient(20) == 8
    try:
        euler_totient(0)
        assert False
    except ValueError:
        pass
    print("euler_totient self-tests passed")
