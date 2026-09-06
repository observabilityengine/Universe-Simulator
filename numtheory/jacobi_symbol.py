"""Jacobi symbol (a/n) for odd positive n.

Complexity: O(log a log n).
Generalizes Legendre; n need not be prime. Original implementation.
"""
from __future__ import annotations


def jacobi_symbol(a: int, n: int) -> int:
    """Compute Jacobi (a/n). n odd positive."""
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be positive odd")
    a %= n
    result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


if __name__ == "__main__":
    assert jacobi_symbol(5, 13) == -1 or jacobi_symbol(5, 13) in (-1, 1)
    assert jacobi_symbol(2, 15) == jacobi_symbol(2, 3) * jacobi_symbol(2, 5)
    assert jacobi_symbol(0, 9) == 0
    assert jacobi_symbol(1, 9) == 1
    try:
        jacobi_symbol(1, 2)
        assert False
    except ValueError:
        pass
    print("jacobi_symbol self-tests passed")
