"""
Universe Simulator - Black-Karasinski short-rate paths
Original lognormal short-rate Euler scheme.
"""

from __future__ import annotations

import math
import random
from typing import List, Callable

def black_karasinski_paths(
    x0: float,
    a: float,
    sigma: float,
    theta: Callable[[float], float],
    t: float,
    steps: int,
    n_paths: int,
    seed: int = 11,
) -> List[List[float]]:
    rng = random.Random(seed)
    dt = t / steps
    sqrt_dt = math.sqrt(dt)
    paths = []
    for _ in range(n_paths):
        x = x0
        path = [math.exp(x)]
        for i in range(steps):
            ti = i * dt
            x = x + (theta(ti) - a * x) * dt + sigma * sqrt_dt * rng.gauss(0, 1)
            path.append(math.exp(x))
        paths.append(path)
    return paths

if __name__ == "__main__":
    paths = black_karasinski_paths(-3.5, 0.1, 0.01, lambda t: 0.0, 1.0, 40, 2)
    assert all(all(r > 0 for r in p) for p in paths)
    print("black_karasinski self-test passed")
