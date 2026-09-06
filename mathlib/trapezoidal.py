"""Composite trapezoidal rule numerical integration.

Complexity: O(n) function evaluations.
Error O(1/n^2) for smooth f. Original implementation.
"""
from __future__ import annotations

from typing import Callable


def trapezoidal(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 100,
) -> float:
    """Approximate ∫_a^b f(x) dx with n subintervals."""
    if n < 1:
        raise ValueError("n >= 1")
    if a == b:
        return 0.0
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h


if __name__ == "__main__":
    est = trapezoidal(lambda x: x * x, 0.0, 1.0, 1000)
    assert abs(est - 1 / 3) < 1e-5
    import math
    est2 = trapezoidal(math.exp, 0.0, 1.0, 500)
    assert abs(est2 - (math.e - 1)) < 1e-4
    assert trapezoidal(lambda x: x, 2.0, 2.0) == 0.0
    try:
        trapezoidal(lambda x: x, 0, 1, 0)
        assert False
    except ValueError:
        pass
    print("trapezoidal self-tests passed")
