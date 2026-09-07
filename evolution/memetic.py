"""Memetic Algorithm (GA + local search).

Complexity: O(pop * (dim + local_steps) * gens). Original implementation.
"""
from __future__ import annotations

import random
from typing import Callable, List, Tuple


def memetic(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    pop_size: int = 20,
    generations: int = 30,
    local_steps: int = 5,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """GA with Lamarckian local search on offspring."""
    rng = random.Random(seed)
    lo, hi = bounds
    pop = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(pop_size)]
    fitness = [objective(ind) for ind in pop]
    best_idx = min(range(pop_size), key=lambda i: fitness[i])
    best = pop[best_idx][:]
    best_fit = fitness[best_idx]

    def local_search(x: List[float]) -> Tuple[List[float], float]:
        current = x[:]
        current_fit = objective(current)
        step = (hi - lo) * 0.05
        for _ in range(local_steps):
            improved = False
            for d in range(dim):
                for direction in (+1, -1):
                    candidate = current[:]
                    candidate[d] = max(lo, min(hi, candidate[d] + direction * step))
                    fit = objective(candidate)
                    if fit < current_fit:
                        current = candidate
                        current_fit = fit
                        improved = True
            if not improved:
                step *= 0.5
        return current, current_fit

    for _ in range(generations):
        new_pop = []
        new_fits = []
        for _ in range(pop_size):
            i1 = min(rng.sample(range(pop_size), 3), key=lambda i: fitness[i])
            i2 = min(rng.sample(range(pop_size), 3), key=lambda i: fitness[i])
            child = [(pop[i1][d] + pop[i2][d]) / 2 for d in range(dim)]
            for d in range(dim):
                if rng.random() < 0.2:
                    child[d] += rng.gauss(0, (hi - lo) * 0.1)
                child[d] = max(lo, min(hi, child[d]))
            child, fit = local_search(child)
            new_pop.append(child)
            new_fits.append(fit)
            if fit < best_fit:
                best = child[:]
                best_fit = fit
        pop = new_pop
        fitness = new_fits
    return best, best_fit


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    best, val = memetic(sphere, dim=3, bounds=(-5, 5), generations=15, seed=8)
    assert val < 1.5
    print("memetic self-tests passed")
