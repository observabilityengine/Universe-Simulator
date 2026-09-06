"""Egyptian fraction expansion (greedy).

Complexity: O(value of denominators) in worst case; practical for moderate inputs.
Expresses a/b as sum of distinct unit fractions. Original implementation.
"""
from __future__ import annotations

from typing import List, Tuple


def egyptian_fraction(num: int, den: int) -> List[Tuple[int, int]]:
    """Return list of (1, d) unit fractions summing to num/den."""
    if den == 0:
        raise ValueError("denominator zero")
    if num == 0:
        return []
    if num < 0 or den < 0:
        raise ValueError("positive fraction required")
    result: List[Tuple[int, int]] = []
    while num > 0:
        # ceil(den/num)
        x = (den + num - 1) // num
        result.append((1, x))
        num = num * x - den
        den = den * x
    return result


if __name__ == "__main__":
    parts = egyptian_fraction(2, 3)
    # 2/3 = 1/2 + 1/6
    assert parts == [(1, 2), (1, 6)]
    assert egyptian_fraction(1, 5) == [(1, 5)]
    assert egyptian_fraction(0, 5) == []
    s = sum(1 / d for _, d in egyptian_fraction(3, 7))
    assert abs(s - 3 / 7) < 1e-10
    print("egyptian_fraction self-tests passed")
