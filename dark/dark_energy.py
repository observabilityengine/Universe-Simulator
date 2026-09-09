"""Dark energy equation of state – w(z) models and expansion effect."""
from __future__ import annotations
import math
from typing import Callable


def w_lambda(z: float) -> float:
    return -1.0


def w_cpl(z: float, w0: float = -0.9, wa: float = 0.1) -> float:
    return w0 + wa * z / (1 + z)


def de_density_evolution(
    a: float,
    w_fn: Callable[[float], float] = w_lambda,
    n_steps: int = 100,
) -> float:
    if a >= 1.0:
        return 1.0
    da = (1.0 - a) / n_steps
    log_ratio = 0.0
    for i in range(n_steps):
        ai = a + (i + 0.5) * da
        z = 1.0 / ai - 1.0
        w = w_fn(z)
        log_ratio += -3 * (1 + w) / ai * da
    return math.exp(log_ratio)


def effective_Ol(z: float, Ol0: float = 0.7, w_fn: Callable[[float], float] = w_lambda) -> float:
    a = 1.0 / (1 + z)
    return Ol0 * de_density_evolution(a, w_fn)


if __name__ == "__main__":
    assert abs(w_lambda(0) + 1) < 1e-12
    r = de_density_evolution(0.5, w_lambda)
    assert abs(r - 1.0) < 1e-6
    r2 = de_density_evolution(0.5, lambda z: w_cpl(z, -0.8, 0.2))
    assert r2 > 0
    print(f"dark_energy rho(a=0.5)/rho0={r:.4f}")
    print("dark_energy self-tests passed")
