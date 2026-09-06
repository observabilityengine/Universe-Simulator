"""LSD radix sort for non-negative integers.

Complexity: O(d * (n + b)) where d = digits, b = base (default 10).
Stable. Only non-negative ints.
"""
from __future__ import annotations

from typing import List


def radix_sort(a: List[int], base: int = 10) -> List[int]:
    """Return sorted copy of non-negative integers."""
    if not a:
        return []
    if any(x < 0 for x in a):
        raise ValueError("radix_sort requires non-negative integers")
    max_val = max(a)
    exp = 1
    result = list(a)
    while max_val // exp > 0:
        result = _counting_by_digit(result, exp, base)
        exp *= base
    return result


def _counting_by_digit(a: List[int], exp: int, base: int) -> List[int]:
    n = len(a)
    count = [0] * base
    for x in a:
        digit = (x // exp) % base
        count[digit] += 1
    for i in range(1, base):
        count[i] += count[i - 1]
    out = [0] * n
    for x in reversed(a):
        digit = (x // exp) % base
        count[digit] -= 1
        out[count[digit]] = x
    return out


if __name__ == "__main__":
    assert radix_sort([170, 45, 75, 90, 802, 24, 2, 66]) == [2, 24, 45, 66, 75, 90, 170, 802]
    assert radix_sort([]) == []
    assert radix_sort([0]) == [0]
    assert radix_sort([5, 5, 5]) == [5, 5, 5]
    assert radix_sort([100, 1, 10, 1000]) == [1, 10, 100, 1000]
    try:
        radix_sort([-1])
        assert False
    except ValueError:
        pass
    print("radix_sort self-tests passed")
