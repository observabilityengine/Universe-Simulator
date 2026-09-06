"""Karatsuba multiplication for non-negative integers.

Complexity: O(n^{log2 3}) ≈ O(n^1.585) for n-digit numbers.
Falls back to built-in for small sizes. Original implementation.
"""
from __future__ import annotations


def karatsuba(x: int, y: int) -> int:
    """Multiply two non-negative integers via Karatsuba."""
    if x < 0 or y < 0:
        raise ValueError("non-negative integers only")
    if x == 0 or y == 0:
        return 0
    if x < 10 or y < 10:
        return x * y
    n = max(x.bit_length(), y.bit_length())
    m = n // 2
    mask = (1 << m) - 1
    x1, x0 = x >> m, x & mask
    y1, y0 = y >> m, y & mask
    z0 = karatsuba(x0, y0)
    z2 = karatsuba(x1, y1)
    z1 = karatsuba(x0 + x1, y0 + y1) - z2 - z0
    return (z2 << (2 * m)) + (z1 << m) + z0


if __name__ == "__main__":
    assert karatsuba(0, 5) == 0
    assert karatsuba(12, 34) == 408
    assert karatsuba(1234, 5678) == 1234 * 5678
    a = 2**128 - 1
    b = 2**64 + 3
    assert karatsuba(a, b) == a * b
    try:
        karatsuba(-1, 2)
        assert False
    except ValueError:
        pass
    print("karatsuba self-tests passed")
