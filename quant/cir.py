"""
Universe Simulator - CIR short-rate model paths
Original Euler with reflection for positivity.
"""

from __future__ import annotations

import math
import random
from typing import List


def cir_paths(
    r0: float,
    kappa: float,
    theta: float,
    sigma: float,
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
        r = r0
        path = [r]
        for _ in range(steps):
            r = r + kappa * (theta - r) * dt + sigma * math.sqrt(max(r, 0.0)) * sqrt_dt * rng.gauss(0, 1)
            r = max(r, 0.0)
            path.append(r)
        paths.append(path)
    return paths


if __name__ == "__main__":
    paths = cir_paths(0.03, 0.4, 0.05, 0.1, 1.0, 40, 3)
    assert all(all(x >= 0 for x in p) for p in paths)
    print("cir self-test passed")
