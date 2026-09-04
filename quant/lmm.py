"""
Universe Simulator - LIBOR Market Model (simple lognormal forward rates)
Original Euler scheme for forward rate dynamics.
"""

from __future__ import annotations

import math
import random
from typing import List

def lmm_paths(
    f0: List[float],
    sigmas: List[float],
    deltas: List[float],
    t: float,
    steps: int,
    n_paths: int,
    seed: int = 42,
) -> List[List[List[float]]]:
    """Returns paths of forward rates [path][time][rate_index]."""
    rng = random.Random(seed)
    n = len(f0)
    dt = t / steps
    sqrt_dt = math.sqrt(dt)
    paths = []
    for _ in range(n_paths):
        f = f0[:]
        path = [f[:]]
        for _ in range(steps):
            for i in range(n):
                drift = 0.0
                for j in range(i + 1):
                    drift += deltas[j] * f[j] * sigmas[j] * sigmas[i] / (1 + deltas[j] * f[j])
                f[i] = f[i] * math.exp((drift - 0.5 * sigmas[i]**2) * dt + sigmas[i] * sqrt_dt * rng.gauss(0, 1))
            path.append(f[:])
        paths.append(path)
    return paths

if __name__ == "__main__":
    f0 = [0.03, 0.032, 0.034]
    sig = [0.2, 0.2, 0.2]
    deltas = [0.5, 0.5, 0.5]
    paths = lmm_paths(f0, sig, deltas, 1.0, 20, 2)
    assert len(paths) == 2 and len(paths[0]) == 21
    print("lmm self-test passed")
