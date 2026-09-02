"""
Universe Simulator - GARCH(1,1) volatility path
Original Euler-style simulation.
"""

from __future__ import annotations

import math
import random
from typing import List, Tuple


def garch11_paths(
    omega: float,
    alpha: float,
    beta: float,
    n_steps: int,
    n_paths: int,
    seed: int = 42,
) -> Tuple[List[List[float]], List[List[float]]]:
    """Returns (returns, conditional_variances)."""
    rng = random.Random(seed)
    rets = []
    vars_ = []
    for _ in range(n_paths):
        r_path = []
        v_path = []
        sigma2 = omega / (1 - alpha - beta) if (alpha + beta) < 1 else omega
        for _ in range(n_steps):
            z = rng.gauss(0, 1)
            r = math.sqrt(max(sigma2, 1e-12)) * z
            sigma2 = omega + alpha * r * r + beta * sigma2
            r_path.append(r)
            v_path.append(sigma2)
        rets.append(r_path)
        vars_.append(v_path)
    return rets, vars_


if __name__ == "__main__":
    r, v = garch11_paths(0.00001, 0.05, 0.9, 100, 3)
    assert len(r) == 3 and len(r[0]) == 100
    assert all(x > 0 for path in v for x in path)
    print("garch self-test passed")
