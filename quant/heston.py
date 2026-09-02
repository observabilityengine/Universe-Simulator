"""
Universe Simulator - Heston Stochastic Volatility (Euler discretisation)
Original path generator for Heston model.
"""

from __future__ import annotations

import math
import random
from typing import List, Tuple


def heston_paths(
    s0: float,
    v0: float,
    kappa: float,
    theta: float,
    xi: float,
    rho: float,
    r: float,
    t: float,
    steps: int,
    n_paths: int,
    seed: int = 42,
) -> Tuple[List[List[float]], List[List[float]]]:
    rng = random.Random(seed)
    dt = t / steps
    sqrt_dt = math.sqrt(dt)
    s_paths = []
    v_paths = []
    for _ in range(n_paths):
        s = s0
        v = v0
        s_path = [s]
        v_path = [v]
        for _ in range(steps):
            z1 = rng.gauss(0, 1)
            z2 = rho * z1 + math.sqrt(1 - rho * rho) * rng.gauss(0, 1)
            v = max(0.0, v + kappa * (theta - v) * dt + xi * math.sqrt(max(v, 0)) * sqrt_dt * z2)
            s = s * math.exp((r - 0.5 * v) * dt + math.sqrt(max(v, 0)) * sqrt_dt * z1)
            s_path.append(s)
            v_path.append(v)
        s_paths.append(s_path)
        v_paths.append(v_path)
    return s_paths, v_paths


if __name__ == "__main__":
    s, v = heston_paths(100, 0.04, 2.0, 0.04, 0.3, -0.7, 0.01, 1.0, 50, 5)
    assert len(s) == 5 and len(s[0]) == 51
    print("heston self-test passed, final S mean ~", sum(p[-1] for p in s) / 5)
