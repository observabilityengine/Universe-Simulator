"""Boolean truth table generator for n-ary functions.

Complexity: O(2^n * cost(fn)).
Original implementation.
"""
from __future__ import annotations

from typing import Callable, List, Tuple


def truth_table(n: int, fn: Callable[..., bool]) -> List[Tuple[Tuple[bool, ...], bool]]:
    """Evaluate fn on all 2^n input combinations."""
    if n < 0 or n > 20:
        raise ValueError("n must be in 0..20")
    rows: List[Tuple[Tuple[bool, ...], bool]] = []
    for mask in range(1 << n):
        inputs = tuple(bool(mask & (1 << (n - 1 - i))) for i in range(n))
        rows.append((inputs, bool(fn(*inputs))))
    return rows


def all_equal(n: int, fn: Callable[..., bool], ref: Callable[..., bool]) -> bool:
    return all(fn(*inp) == ref(*inp) for inp, _ in truth_table(n, fn))


if __name__ == "__main__":
    tt = truth_table(2, lambda a, b: a and b)
    assert len(tt) == 4
    assert tt[3] == ((True, True), True)
    assert tt[0] == ((False, False), False)
    assert all_equal(2, lambda a, b: a or b, lambda a, b: a or b)
    assert truth_table(0, lambda: True) == [((), True)]
    print("truth_table self-tests passed")
