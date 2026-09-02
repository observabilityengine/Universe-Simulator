"""
Module 67 – Monte Carlo Integration & Option Pricing
Crude MC integrator + European option via risk-neutral simulation.
Complete quantitative implementation.
"""

from __future__ import annotations
import math
import random
from typing import Callable, Tuple


def mc_integrate(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 100_000,
    seed: int | None = None,
) -> Tuple[float, float]:
    rng = random.Random(seed)
    total = 0.0
    total_sq = 0.0
    for _ in range(n):
        x = a + (b - a) * rng.random()
        y = f(x)
        total += y
        total_sq += y * y
    mean = total / n
    var = total_sq / n - mean * mean
    estimate = (b - a) * mean
    se = (b - a) * math.sqrt(max(var, 0.0) / n)
    return estimate, se


def mc_european_call(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    n_paths: int = 50_000,
    seed: int | None = None,
) -> Tuple[float, float]:
    rng = random.Random(seed)
    payoff_sum = 0.0
    payoff_sq = 0.0
    drift = (r - 0.5 * sigma * sigma) * T
    vol = sigma * math.sqrt(T)
    for _ in range(n_paths):
        z = rng.gauss(0, 1)
        ST = S0 * math.exp(drift + vol * z)
        payoff = max(ST - K, 0.0)
        payoff_sum += payoff
        payoff_sq += payoff * payoff
    mean = payoff_sum / n_paths
    var = payoff_sq / n_paths - mean * mean
    price = math.exp(-r * T) * mean
    se = math.exp(-r * T) * math.sqrt(max(var, 0.0) / n_paths)
    return price, se


if __name__ == "__main__":
    print("Testing Monte Carlo...")
    est, se = mc_integrate(lambda x: x * x, 0, 1, n=100000, seed=42)
    print(f"  \u222bx\u00b2 dx [0,1] \u2248 {est:.5f} \u00b1 {se:.5f} (true 0.33333)")
    price, se_p = mc_european_call(100, 100, 1.0, 0.05, 0.2, n_paths=50000, seed=1)
    print(f"  MC Call price \u2248 {price:.4f} \u00b1 {se_p:.4f}")
    print("Monte Carlo module OK.")
