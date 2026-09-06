"""Integer square root via binary search / Newton's method.

Complexity: O(log n).
Returns floor(sqrt(n)) for n >= 0. Original implementation.
"""
from __future__ import annotations


def isqrt(n: int) -> int:
    """Largest integer r with r*r <= n."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    # Newton's method for integer sqrt
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


if __name__ == "__main__":
    assert isqrt(0) == 0
    assert isqrt(1) == 1
    assert isqrt(15) == 3
    assert isqrt(16) == 4
    assert isqrt(100) == 10
    assert isqrt(10**18) == 10**9
    try:
        isqrt(-1)
        assert False
    except ValueError:
        pass
    print("isqrt self-tests passed")
