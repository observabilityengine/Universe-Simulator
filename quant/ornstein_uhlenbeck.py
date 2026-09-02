"""
Universe Simulator - Ornstein-Uhlenbeck process paths
Original exact discretization.
"""

from __future__ import annotations

import math
import random
from typing import List


def ou_paths(
    x0: float,
    theta: float,
    mu: float,
    sigma: float,
    t: float,
    steps: int,
    n_paths: int,
    seed: int = 1,
) -> List[List[float]]:
    rng = random.Random(seed)
    dt = t / steps
    exp_term = math.exp(-theta * dt)
    paths = []
    for _ in range(n_paths):
        x = x0
        path = [x]
        for _ in range(steps):
            noise = sigma * math.sqrt((1 - exp_term ** 2) / (2 * theta)) * rng.gauss(0, 1)
            x = x * exp_term + mu * (1 - exp_term) + noise
            path.append(x)
        paths.append(path)
    return paths


if __name__ == "__main__":
    paths = ou_paths(0.0, 1.0, 0.5, 0.2, 2.0, 50, 4)
    assert len(paths) == 4 and len(paths[0]) == 51
    print("ornstein_uhlenbeck self-test passed", sum(p[-1] for p in paths) / 4)
