"""Ternary search for unimodal function minimum on continuous interval.

Complexity: O(log((r-l)/eps)) evaluations.
Assumes f is unimodal (decreases then increases) on [lo, hi].
Original implementation.
"""
from __future__ import annotations

from typing import Callable, Tuple


def ternary_search(
    f: Callable[[float], float],
    lo: float,
    hi: float,
    eps: float = 1e-9,
    max_iter: int = 200,
) -> Tuple[float, float]:
    """Return (x_min, f(x_min)) approximating the minimum of unimodal f."""
    if lo > hi:
        raise ValueError("lo > hi")
    for _ in range(max_iter):
        if hi - lo < eps:
            break
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if f(m1) < f(m2):
            hi = m2
        else:
            lo = m1
    x = (lo + hi) / 2
    return x, f(x)


if __name__ == "__main__":
    # f(x) = (x-3)^2 + 1  minimum at x=3, f=1
    f = lambda x: (x - 3) ** 2 + 1
    x, fx = ternary_search(f, 0.0, 6.0)
    assert abs(x - 3.0) < 1e-5
    assert abs(fx - 1.0) < 1e-5
    # constant
    x2, fx2 = ternary_search(lambda x: 5.0, -1.0, 1.0)
    assert abs(fx2 - 5.0) < 1e-12
    try:
        ternary_search(f, 5.0, 1.0)
        assert False
    except ValueError:
        pass
    print("ternary_search self-tests passed")
