"""Limited-memory BFGS (L-BFGS) optimizer.

Complexity: O(m * dim) per iteration. Original implementation.
"""
from __future__ import annotations

from typing import Callable, List, Tuple
import math


def lbfgs(
    f: Callable[[List[float]], float],
    grad: Callable[[List[float]], List[float]],
    x0: List[float],
    max_iter: int = 100,
    m: int = 10,
    tol: float = 1e-6,
    line_search_max: int = 20,
) -> Tuple[List[float], float]:
    n = len(x0)
    x = x0[:]
    g = grad(x)
    fval = f(x)
    s_hist: List[List[float]] = []
    y_hist: List[List[float]] = []
    rho_hist: List[float] = []

    for _ in range(max_iter):
        gnorm = math.sqrt(sum(gi * gi for gi in g))
        if gnorm < tol:
            break
        q = g[:]
        alpha_list = []
        for i in range(len(s_hist) - 1, -1, -1):
            alpha = rho_hist[i] * sum(s_hist[i][j] * q[j] for j in range(n))
            alpha_list.append(alpha)
            q = [q[j] - alpha * y_hist[i][j] for j in range(n)]
        alpha_list.reverse()
        if s_hist:
            ys = sum(y_hist[-1][j] * s_hist[-1][j] for j in range(n))
            yy = sum(y_hist[-1][j] * y_hist[-1][j] for j in range(n))
            gamma = ys / yy if yy > 1e-12 else 1.0
        else:
            gamma = 1.0
        r = [gamma * qj for qj in q]
        for i in range(len(s_hist)):
            beta = rho_hist[i] * sum(y_hist[i][j] * r[j] for j in range(n))
            r = [r[j] + s_hist[i][j] * (alpha_list[i] - beta) for j in range(n)]
        direction = [-ri for ri in r]
        step = 1.0
        c1 = 1e-4
        gdotd = sum(g[j] * direction[j] for j in range(n))
        for _ in range(line_search_max):
            x_new = [x[j] + step * direction[j] for j in range(n)]
            f_new = f(x_new)
            if f_new <= fval + c1 * step * gdotd:
                break
            step *= 0.5
        else:
            step = 1e-6
            x_new = [x[j] + step * direction[j] for j in range(n)]
            f_new = f(x_new)
        g_new = grad(x_new)
        s = [x_new[j] - x[j] for j in range(n)]
        y = [g_new[j] - g[j] for j in range(n)]
        ys = sum(y[j] * s[j] for j in range(n))
        if ys > 1e-12:
            if len(s_hist) == m:
                s_hist.pop(0)
                y_hist.pop(0)
                rho_hist.pop(0)
            s_hist.append(s)
            y_hist.append(y)
            rho_hist.append(1.0 / ys)
        x, g, fval = x_new, g_new, f_new
    return x, fval


if __name__ == "__main__":
    def rosenbrock(x: List[float]) -> float:
        return (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2

    def rosenbrock_grad(x: List[float]) -> List[float]:
        d0 = -2 * (1 - x[0]) - 400 * x[0] * (x[1] - x[0] ** 2)
        d1 = 200 * (x[1] - x[0] ** 2)
        return [d0, d1]

    xopt, fopt = lbfgs(rosenbrock, rosenbrock_grad, [-1.0, 1.0], max_iter=200)
    assert fopt < 1e-4, fopt
    assert abs(xopt[0] - 1.0) < 0.05
    assert abs(xopt[1] - 1.0) < 0.05
    print("lbfgs self-tests passed")
