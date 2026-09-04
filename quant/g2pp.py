"""
Universe Simulator - G2++ two-factor short-rate model paths
Original Euler discretisation.
"""

from __future__ import annotations

import math
import random
from typing import List, Tuple

def g2pp_paths(
    x0: float, y0: float,
    a: float, b: float,
    sigma: float, eta: float,
    rho: float,
    t: float, steps: int, n_paths: int,
    seed: int = 42,
) -> List[List[float]]:
    rng = random.Random(seed)
    dt = t / steps
    sqrt_dt = math.sqrt(dt)
    paths = []
    for _ in range(n_paths):
        x, y = x0, y0
        path = [x + y]
        for _ in range(steps):
            z1 = rng.gauss(0, 1)
            z2 = rho * z1 + math.sqrt(1 - rho * rho) * rng.gauss(0, 1)
            x = x - a * x * dt + sigma * sqrt_dt * z1
            y = y - b * y * dt + eta * sqrt_dt * z2
            path.append(x + y)
        paths.append(path)
    return paths

if __name__ == "__main__":
    paths = g2pp_paths(0.01, 0.01, 0.5, 0.3, 0.01, 0.01, -0.5, 1.0, 40, 3)
    assert len(paths) == 3 and len(paths[0]) == 41
    print("g2pp self-test passed")
