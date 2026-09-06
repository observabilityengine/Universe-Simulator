"""Newton-Raphson root finding for scalar functions.

Complexity: quadratic convergence near simple roots; may diverge.
Requires f and f'. Stops on |f(x)| < tol or max_iter.
"""
from __future__ import annotations

from typing import Callable, Tuple


def newton_raphson(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    tol: float = 1e-12,
    max_iter: int = 100,
) -> Tuple[float, int]:
    """Return (root, iterations). Raises RuntimeError on failure."""
    x = x0
    for i in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x, i
        dfx = df(x)
        if abs(dfx) < 1e-15:
            raise RuntimeError("derivative near zero")
        x = x - fx / dfx
    raise RuntimeError("max iterations exceeded")


if __name__ == "__main__":
    f = lambda x: x * x - 2
    df = lambda x: 2 * x
    root, iters = newton_raphson(f, df, 1.0)
    assert abs(root - 2**0.5) < 1e-10
    f2 = lambda x: x**3 - 27
    df2 = lambda x: 3 * x**2
    root2, _ = newton_raphson(f2, df2, 2.0)
    assert abs(root2 - 3.0) < 1e-10
    root3, iters3 = newton_raphson(lambda x: x - 5, lambda x: 1.0, 5.0)
    assert abs(root3 - 5) < 1e-15 and iters3 == 0
    try:
        newton_raphson(lambda x: x**2 + 1, lambda x: 2 * x, 0.0)
        assert False
    except RuntimeError:
        pass
    print("newton_raphson self-tests passed")
