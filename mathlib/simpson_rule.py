"""Composite Simpson's rule numerical integration.

Complexity: O(n) function evaluations for n subintervals (n even).
Error O(1/n^4) for smooth f. Original implementation.
"""
from __future__ import annotations

from typing import Callable


def simpson_rule(f: Callable[[float], float], a: float, b: float, n: int = 100) -> float:
    """Approximate ∫_a^b f(x) dx with composite Simpson (n even)."""
    if n < 2 or n % 2 != 0:
        raise ValueError("n must be even and >= 2")
    if a == b:
        return 0.0
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        s += (4 if i % 2 else 2) * f(x)
    return s * h / 3


if __name__ == "__main__":
    # ∫_0^1 x^2 dx = 1/3
    est = simpson_rule(lambda x: x * x, 0.0, 1.0, 100)
    assert abs(est - 1 / 3) < 1e-8
    # ∫_0^π sin = 2
    est2 = simpson_rule(lambda x: __import__("math").sin(x), 0.0, __import__("math").pi, 200)
    assert abs(est2 - 2.0) < 1e-6
    assert simpson_rule(lambda x: 1.0, 5.0, 5.0) == 0.0
    try:
        simpson_rule(lambda x: x, 0, 1, 3)
        assert False
    except ValueError:
        pass
    print("simpson_rule self-tests passed")
