"""Firefly Algorithm.

Complexity: O(pop^2 * dim * iters). Original implementation.
"""
from __future__ import annotations

import math
import random
from typing import Callable, List, Tuple


def firefly(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    n_fireflies: int = 20,
    iterations: int = 40,
    alpha: float = 0.2,
    beta0: float = 1.0,
    gamma: float = 1.0,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """Minimize with Firefly Algorithm."""
    rng = random.Random(seed)
    lo, hi = bounds
    pop = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(n_fireflies)]
    fitness = [objective(p) for p in pop]

    best_idx = min(range(n_fireflies), key=lambda i: fitness[i])
    best = pop[best_idx][:]
    best_fit = fitness[best_idx]

    for _ in range(iterations):
        for i in range(n_fireflies):
            for j in range(n_fireflies):
                if fitness[j] < fitness[i]:
                    r2 = sum((pop[i][d] - pop[j][d]) ** 2 for d in range(dim))
                    beta = beta0 * math.exp(-gamma * r2)
                    for d in range(dim):
                        pop[i][d] += beta * (pop[j][d] - pop[i][d]) + alpha * (rng.random() - 0.5)
                        pop[i][d] = max(lo, min(hi, pop[i][d]))
            fitness[i] = objective(pop[i])
            if fitness[i] < best_fit:
                best = pop[i][:]
                best_fit = fitness[i]
        alpha *= 0.97
    return best, best_fit


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    best, val = firefly(sphere, dim=3, bounds=(-5, 5), iterations=30, seed=2)
    assert val < 2.0
    print("firefly self-tests passed")
