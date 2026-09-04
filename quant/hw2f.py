"""
Universe Simulator - Hull-White 2-Factor short-rate paths
Original Euler scheme for two-factor model.
"""

from __future__ import annotations

import math
import random
from typing import List, Callable

def hw2f_paths(
    x0: float, y0: float,
    a: float, b: float,
    sigma: float, eta: float,
    rho: float,
    theta: Callable[[float], float],
    t: float, steps: int, n_paths: int, seed: int = 42,
) -> List[List[float]]:
    rng = random.Random(seed)
    dt = t / steps
    sqrt_dt = math.sqrt(dt)
    paths = []
    for _ in range(n_paths):
        x, y = x0, y0
        path = [x + y]
        for i in range(steps):
            z1 = rng.gauss(0, 1)
            z2 = rho * z1 + math.sqrt(max(0, 1 - rho*rho)) * rng.gauss(0, 1)
            x = x + (theta(i*dt) - a * x) * dt + sigma * sqrt_dt * z1
            y = y - b * y * dt + eta * sqrt_dt * z2
            path.append(x + y)
        paths.append(path)
    return paths

if __name__ == "__main__":
    paths = hw2f_paths(0.01, 0.01, 0.1, 0.2, 0.01, 0.01, -0.3, lambda t: 0.02, 1.0, 30, 2)
    assert len(paths) == 2 and len(paths[0]) == 31
    print("hw2f self-test passed")
