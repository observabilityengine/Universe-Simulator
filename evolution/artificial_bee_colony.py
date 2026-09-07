"""Artificial Bee Colony (ABC) algorithm.

Complexity: O(pop * dim * iters). Original implementation.
"""
from __future__ import annotations

import random
from typing import Callable, List, Tuple


def artificial_bee_colony(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    n_bees: int = 20,
    iterations: int = 40,
    limit: int = 10,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """Minimize with Artificial Bee Colony."""
    rng = random.Random(seed)
    lo, hi = bounds
    foods = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(n_bees)]
    fitness = [objective(f) for f in foods]
    trials = [0] * n_bees
    best_idx = min(range(n_bees), key=lambda i: fitness[i])
    best = foods[best_idx][:]
    best_fit = fitness[best_idx]

    def employed_phase():
        nonlocal best, best_fit
        for i in range(n_bees):
            k = rng.randrange(n_bees)
            while k == i:
                k = rng.randrange(n_bees)
            phi = rng.uniform(-1, 1)
            j = rng.randrange(dim)
            new = foods[i][:]
            new[j] = foods[i][j] + phi * (foods[i][j] - foods[k][j])
            new[j] = max(lo, min(hi, new[j]))
            new_fit = objective(new)
            if new_fit < fitness[i]:
                foods[i] = new
                fitness[i] = new_fit
                trials[i] = 0
                if new_fit < best_fit:
                    best = new[:]
                    best_fit = new_fit
            else:
                trials[i] += 1

    def onlooker_phase():
        nonlocal best, best_fit
        max_fit = max(fitness)
        probs = [(max_fit - f + 1e-12) for f in fitness]
        total = sum(probs)
        probs = [p / total for p in probs]
        for _ in range(n_bees):
            r = rng.random()
            cum = 0.0
            i = 0
            for idx, p in enumerate(probs):
                cum += p
                if r <= cum:
                    i = idx
                    break
            k = rng.randrange(n_bees)
            while k == i:
                k = rng.randrange(n_bees)
            phi = rng.uniform(-1, 1)
            j = rng.randrange(dim)
            new = foods[i][:]
            new[j] = foods[i][j] + phi * (foods[i][j] - foods[k][j])
            new[j] = max(lo, min(hi, new[j]))
            new_fit = objective(new)
            if new_fit < fitness[i]:
                foods[i] = new
                fitness[i] = new_fit
                trials[i] = 0
                if new_fit < best_fit:
                    best = new[:]
                    best_fit = new_fit
            else:
                trials[i] += 1

    def scout_phase():
        for i in range(n_bees):
            if trials[i] >= limit:
                foods[i] = [rng.uniform(lo, hi) for _ in range(dim)]
                fitness[i] = objective(foods[i])
                trials[i] = 0

    for _ in range(iterations):
        employed_phase()
        onlooker_phase()
        scout_phase()
    return best, best_fit


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    best, val = artificial_bee_colony(sphere, dim=4, bounds=(-5, 5), iterations=30, seed=5)
    assert val < 2.0
    print("artificial_bee_colony self-tests passed")
