"""Quantile / percentile estimation (linear interpolation, type 7).

Complexity: O(n log n) due to sort.
Original implementation.
"""
from __future__ import annotations

from typing import List, Sequence


def quantile(data: Sequence[float], q: float) -> float:
    """q in [0, 1]. R-7 / NumPy default style."""
    if not data:
        raise ValueError("empty data")
    if not 0 <= q <= 1:
        raise ValueError("q must be in [0, 1]")
    xs = sorted(data)
    n = len(xs)
    if n == 1:
        return xs[0]
    h = (n - 1) * q
    lo = int(h)
    hi = min(lo + 1, n - 1)
    frac = h - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def quantiles(data: Sequence[float], qs: Sequence[float]) -> List[float]:
    return [quantile(data, q) for q in qs]


if __name__ == "__main__":
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    assert abs(quantile(data, 0.5) - 3.0) < 1e-12
    assert abs(quantile(data, 0.0) - 1.0) < 1e-12
    assert abs(quantile(data, 1.0) - 5.0) < 1e-12
    assert abs(quantile([7.0], 0.3) - 7.0) < 1e-12
    print("quantile self-tests passed")
