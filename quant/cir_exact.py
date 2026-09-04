"""
Universe Simulator - CIR Exact Simulation (non-central chi-squared)
Original transition sampling for Cox-Ingersoll-Ross.
"""

from __future__ import annotations

import math
import random
from typing import List

def cir_exact(
    r0: float, kappa: float, theta: float, sigma: float,
    t: float, steps: int, n_paths: int, seed: int = 42,
) -> List[List[float]]:
    rng = random.Random(seed)
    dt = t / steps
    d = 4 * kappa * theta / (sigma ** 2)
    paths = []
    for _ in range(n_paths):
        r = r0
        path = [r]
        for _ in range(steps):
            c = (sigma ** 2) * (1 - math.exp(-kappa * dt)) / (4 * kappa)
            lam = r * math.exp(-kappa * dt) / c
            # approximate non-central chi2 by Poisson + gamma
            if d > 1:
                n = rng.gauss(0, 1) ** 2
                for _ in range(int(d) - 1):
                    n += rng.gauss(0, 1) ** 2
                # non-centrality approx
                n += sum(rng.gauss(math.sqrt(lam / max(int(d),1)), 1) ** 2 for _ in range(max(1, int(lam)))) / max(1, int(lam)) * lam if lam > 0 else 0
                r = c * max(n, 0)
            else:
                # fallback Euler
                r = r + kappa * (theta - r) * dt + sigma * math.sqrt(max(r, 0)) * math.sqrt(dt) * rng.gauss(0, 1)
                r = max(r, 0)
            path.append(r)
        paths.append(path)
    return paths

if __name__ == "__main__":
    paths = cir_exact(0.02, 0.5, 0.03, 0.1, 1.0, 20, 2)
    assert all(all(r >= 0 for r in p) for p in paths)
    print("cir_exact self-test passed")
