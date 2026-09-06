"""Binomial coefficient C(n, k) via multiplicative formula.

Complexity: O(k) multiplications with reductions.
Handles n >= 0, 0 <= k <= n; returns 0 if k > n. Original implementation.
"""
from __future__ import annotations


def binomial(n: int, k: int) -> int:
    """Return C(n, k)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result


if __name__ == "__main__":
    assert binomial(5, 2) == 10
    assert binomial(10, 0) == 1
    assert binomial(10, 10) == 1
    assert binomial(10, 3) == 120
    assert binomial(0, 0) == 1
    assert binomial(5, 6) == 0
    assert binomial(100, 2) == 4950
    try:
        binomial(-1, 0)
        assert False
    except ValueError:
        pass
    print("binomial self-tests passed")
