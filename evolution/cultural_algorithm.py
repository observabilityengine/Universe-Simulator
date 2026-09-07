"""Cultural Algorithm (population + belief space).

Complexity: O(pop * dim * gens). Original implementation.
"""
from __future__ import annotations

import random
from typing import Callable, List, Tuple


def cultural_algorithm(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    pop_size: int = 20,
    generations: int = 40,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """Cultural Algorithm with situational and normative knowledge."""
    rng = random.Random(seed)
    lo, hi = bounds
    pop = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(pop_size)]
    fitness = [objective(ind) for ind in pop]

    norm_min = [lo] * dim
    norm_max = [hi] * dim
    best_idx = min(range(pop_size), key=lambda i: fitness[i])
    situational = pop[best_idx][:]
    best_fit = fitness[best_idx]

    for _ in range(generations):
        for i in range(pop_size):
            for d in range(dim):
                if rng.random() < 0.5:
                    pop[i][d] = rng.uniform(norm_min[d], norm_max[d])
                else:
                    pop[i][d] += rng.gauss(0, abs(situational[d] - pop[i][d]) * 0.2 + 1e-6)
                pop[i][d] = max(lo, min(hi, pop[i][d]))
            fitness[i] = objective(pop[i])
            if fitness[i] < best_fit:
                situational = pop[i][:]
                best_fit = fitness[i]

        order = sorted(range(pop_size), key=lambda i: fitness[i])
        accept = max(2, pop_size // 5)
        for d in range(dim):
            vals = [pop[order[k]][d] for k in range(accept)]
            norm_min[d] = min(vals)
            norm_max[d] = max(vals)
    return situational, best_fit


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    best, val = cultural_algorithm(sphere, dim=3, bounds=(-5, 5), generations=30, seed=12)
    assert val < 2.0
    print("cultural_algorithm self-tests passed")
