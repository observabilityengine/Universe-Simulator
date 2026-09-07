"""Simplified CMA-ES (Covariance Matrix Adaptation Evolution Strategy).

Complexity: O(pop * dim^2 * gens) approximate. Original educational implementation.
"""
from __future__ import annotations

import math
import random
from typing import Callable, List, Tuple


def cmaes_simple(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    pop_size: int | None = None,
    generations: int = 40,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """Simplified CMA-ES (diagonal covariance + rank-mu update)."""
    rng = random.Random(seed)
    lo, hi = bounds
    if pop_size is None:
        pop_size = 4 + int(3 * math.log(dim))
    mu = pop_size // 2

    mean = [(lo + hi) / 2] * dim
    sigma = (hi - lo) * 0.3
    C = [1.0] * dim
    pc = [0.0] * dim

    weights = [math.log(mu + 0.5) - math.log(i + 1) for i in range(mu)]
    wsum = sum(weights)
    weights = [w / wsum for w in weights]
    mueff = 1.0 / sum(w * w for w in weights)

    cc = 4.0 / (dim + 4)
    cs = (mueff + 2) / (dim + mueff + 5)
    c1 = 2.0 / ((dim + 1.3) ** 2 + mueff)
    cmu = min(1 - c1, 2 * (mueff - 2 + 1 / mueff) / ((dim + 2) ** 2 + mueff))
    damps = 1 + 2 * max(0, math.sqrt((mueff - 1) / (dim + 1)) - 1) + cs

    best = mean[:]
    best_fit = objective(mean)
    chiN = math.sqrt(dim) * (1 - 1 / (4 * dim) + 1 / (21 * dim ** 2))

    for _ in range(generations):
        pop = []
        for _ in range(pop_size):
            z = [rng.gauss(0, 1) for _ in range(dim)]
            x = [mean[d] + sigma * math.sqrt(C[d]) * z[d] for d in range(dim)]
            x = [max(lo, min(hi, v)) for v in x]
            pop.append((x, objective(x), z))
        pop.sort(key=lambda t: t[1])
        if pop[0][1] < best_fit:
            best = pop[0][0][:]
            best_fit = pop[0][1]

        old_mean = mean[:]
        mean = [0.0] * dim
        for i in range(mu):
            for d in range(dim):
                mean[d] += weights[i] * pop[i][0][d]

        for d in range(dim):
            pc[d] = (1 - cc) * pc[d] + math.sqrt(cc * (2 - cc) * mueff) * (mean[d] - old_mean[d]) / (sigma + 1e-12)

        for d in range(dim):
            C[d] = (1 - c1 - cmu) * C[d] + c1 * pc[d] ** 2
            for i in range(mu):
                C[d] += cmu * weights[i] * pop[i][2][d] ** 2
            C[d] = max(C[d], 1e-8)

        sigma *= math.exp(min(1.0, (cs / damps) * (math.sqrt(sum(pc[d]**2 for d in range(dim))) / chiN - 1)))
        sigma = max(1e-8, min(sigma, (hi - lo)))

    return best, best_fit


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    best, val = cmaes_simple(sphere, dim=4, bounds=(-5, 5), generations=25, seed=9)
    assert val < 2.0
    print("cmaes_simple self-tests passed")
