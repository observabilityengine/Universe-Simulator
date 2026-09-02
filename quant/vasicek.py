"""
Universe Simulator - Vasicek short-rate model paths
Original Euler discretisation.
"""

from __future__ import annotations

import math
import random
from typing import List


def vasicek_paths(
    r0: float,
    kappa: float,
    theta: float,
    sigma: float,
    t: float,
    steps: int,
    n_paths: int,
    seed: int = 42,
) -> List[List[float]]:
    rng = random.Random(seed)
    dt = t / steps
    sqrt_dt = math.sqrt(dt)
    paths = []
    for _ in range(n_paths):
        r = r0
        path = [r]
        for _ in range(steps):
            r = r + kappa * (theta - r) * dt + sigma * sqrt_dt * rng.gauss(0, 1)
            path.append(r)
        paths.append(path)
    return paths


if __name__ == "__main__":
    paths = vasicek_paths(0.03, 0.5, 0.05, 0.01, 1.0, 50, 4)
    assert len(paths) == 4 and len(paths[0]) == 51
    print("vasicek self-test passed, final mean ~", sum(p[-1] for p in paths) / 4)
