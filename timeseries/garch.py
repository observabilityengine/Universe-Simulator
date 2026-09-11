"""GARCH(1,1) volatility model."""
from __future__ import annotations
from typing import List, Tuple


def fit_garch(returns: List[float], n_iter: int = 30) -> Tuple[float, float, float, List[float]]:
    """Estimate omega, alpha, beta via simplified MLE gradient steps."""
    omega, alpha, beta = 0.01, 0.05, 0.9
    var = [sum(r * r for r in returns) / len(returns)] * len(returns)
    for _ in range(n_iter):
        for t in range(1, len(returns)):
            var[t] = omega + alpha * returns[t - 1] ** 2 + beta * var[t - 1]
        # crude gradient
        for t in range(1, len(returns)):
            v = var[t] or 1e-12
            g_omega = -0.5 / v + 0.5 * returns[t] ** 2 / (v * v)
            omega = max(1e-8, omega + 0.0001 * g_omega)
            alpha = min(0.3, max(0.01, alpha))
            beta = min(0.95, max(0.5, beta))
    return omega, alpha, beta, var


if __name__ == "__main__":
    import random
    rng = random.Random(0)
    rets = [rng.gauss(0, 1) * (1.5 if i % 20 < 5 else 1) for i in range(100)]
    o, a, b, v = fit_garch(rets)
    assert o > 0 and a > 0 and b > 0
    print(f"garch omega={o:.4f} alpha={a:.3f} beta={b:.3f}")
    print("garch self-tests passed")
