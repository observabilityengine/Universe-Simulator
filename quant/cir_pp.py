"""
Universe Simulator - CIR++ short-rate model paths
Original with deterministic shift.
"""

from __future__ import annotations

import math
import random
from typing import List, Callable

def cir_pp_paths(
    x0: float,
    kappa: float,
    theta: float,
    sigma: float,
    phi: Callable[[float], float],
    t: float,
    steps: int,
    n_paths: int,
    seed: int = 7,
) -> List[List[float]]:
    rng = random.Random(seed)
    dt = t / steps
    sqrt_dt = math.sqrt(dt)
    paths = []
    for _ in range(n_paths):
        x = x0
        path = [x + phi(0.0)]
        for i in range(steps):
            x = x + kappa * (theta - x) * dt + sigma * math.sqrt(max(x, 0)) * sqrt_dt * rng.gauss(0, 1)
            x = max(x, 0.0)
            path.append(x + phi((i + 1) * dt))
        paths.append(path)
    return paths

if __name__ == "__main__":
    paths = cir_pp_paths(0.01, 0.5, 0.02, 0.1, lambda t: 0.01, 1.0, 40, 2)
    assert all(all(r >= 0 for r in p) for p in paths)
    print("cir_pp self-test passed")
