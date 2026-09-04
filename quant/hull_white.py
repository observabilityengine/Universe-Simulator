"""
Universe Simulator - Hull-White 1F short-rate paths
Original Euler discretisation with time-dependent theta.
"""

from __future__ import annotations

import math
import random
from typing import List, Callable

def hull_white_paths(
    r0: float,
    a: float,
    sigma: float,
    theta: Callable[[float], float],
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
        for i in range(steps):
            ti = i * dt
            r = r + (theta(ti) - a * r) * dt + sigma * sqrt_dt * rng.gauss(0, 1)
            path.append(r)
        paths.append(path)
    return paths

if __name__ == "__main__":
    paths = hull_white_paths(0.03, 0.1, 0.01, lambda t: 0.03, 1.0, 50, 3)
    assert len(paths) == 3 and len(paths[0]) == 51
    print("hull_white self-test passed")
