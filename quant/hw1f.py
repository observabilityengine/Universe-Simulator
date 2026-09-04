"""
Universe Simulator - Hull-White 1F with analytic bond pricing
Original short-rate paths + zero-bond formula under HW1F.
"""

from __future__ import annotations

import math
import random
from typing import List, Callable

def hw1f_paths(
    r0: float, a: float, sigma: float,
    theta: Callable[[float], float],
    t: float, steps: int, n_paths: int, seed: int = 42,
) -> List[List[float]]:
    rng = random.Random(seed)
    dt = t / steps
    sqrt_dt = math.sqrt(dt)
    paths = []
    for _ in range(n_paths):
        r = r0
        path = [r]
        for i in range(steps):
            ti = i * dt
            r = r + (theta(ti) - a * r) * dt + sigma * sqrt_dt * rng.gauss(0, 1)
            path.append(r)
        paths.append(path)
    return paths

def hw1f_bond_price(r: float, t: float, T: float, a: float, sigma: float, P0t: float, P0T: float) -> float:
    """Affine bond price P(t,T) under HW1F given current short rate r."""
    B = (1 - math.exp(-a * (T - t))) / a if a > 1e-12 else (T - t)
    A = (P0T / P0t) * math.exp(B * (math.exp(-a * t) - 1) * (sigma ** 2) / (2 * a) - (sigma ** 2) * B ** 2 / (4 * a))
    return A * math.exp(-B * r)

if __name__ == "__main__":
    paths = hw1f_paths(0.03, 0.1, 0.01, lambda t: 0.03, 1.0, 30, 2)
    assert len(paths[0]) == 31
    p = hw1f_bond_price(0.03, 0.0, 1.0, 0.1, 0.01, 1.0, 0.97)
    assert 0.9 < p < 1.0
    print("hw1f self-test passed", p)
