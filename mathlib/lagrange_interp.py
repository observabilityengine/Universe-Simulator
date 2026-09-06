"""Lagrange polynomial interpolation.

Complexity: O(n^2) evaluation for n points.
Given distinct x_i, returns value of unique degree <n polynomial at query points.
"""
from __future__ import annotations

from typing import List, Sequence


def lagrange_interp(x: Sequence[float], y: Sequence[float], xq: Sequence[float]) -> List[float]:
    """Interpolate (x, y) data and evaluate at xq."""
    n = len(x)
    if n != len(y) or n == 0:
        raise ValueError("x and y must be non-empty equal length")
    if len(set(x)) != n:
        raise ValueError("x values must be distinct")
    result = []
    for q in xq:
        s = 0.0
        for i in range(n):
            term = y[i]
            for j in range(n):
                if i != j:
                    term *= (q - x[j]) / (x[i] - x[j])
            s += term
        result.append(s)
    return result


if __name__ == "__main__":
    assert abs(lagrange_interp([0, 1], [0, 1], [0.5])[0] - 0.5) < 1e-12
    xs = [0., 1., 2.]
    ys = [0., 1., 4.]
    vals = lagrange_interp(xs, ys, [0.5, 1.5, 3.0])
    assert abs(vals[0] - 0.25) < 1e-10
    assert abs(vals[1] - 2.25) < 1e-10
    assert abs(vals[2] - 9.0) < 1e-10
    assert lagrange_interp([5.], [7.], [0., 10.]) == [7., 7.]
    try:
        lagrange_interp([1, 1], [2, 3], [0])
        assert False
    except ValueError:
        pass
    try:
        lagrange_interp([], [], [0])
        assert False
    except ValueError:
        pass
    print("lagrange_interp self-tests passed")
