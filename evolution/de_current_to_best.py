"""Differential Evolution current-to-best/1/bin variant.

Complexity: O(pop * dim * gens). Original implementation.
"""
from __future__ import annotations

import random
from typing import Callable, List, Tuple


def de_current_to_best(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    pop_size: int = 20,
    generations: int = 50,
    F: float = 0.7,
    CR: float = 0.9,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """DE/current-to-best/1/bin."""
    rng = random.Random(seed)
    lo, hi = bounds
    pop = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(pop_size)]
    fitness = [objective(ind) for ind in pop]
    best_idx = min(range(pop_size), key=lambda i: fitness[i])
    best = pop[best_idx][:]
    best_fit = fitness[best_idx]

    for _ in range(generations):
        for i in range(pop_size):
            idxs = [j for j in range(pop_size) if j != i]
            r1, r2 = rng.sample(idxs, 2)
            mutant = []
            for d in range(dim):
                val = pop[i][d] + F * (best[d] - pop[i][d]) + F * (pop[r1][d] - pop[r2][d])
                mutant.append(max(lo, min(hi, val)))
            trial = []
            j_rand = rng.randrange(dim)
            for d in range(dim):
                if rng.random() < CR or d == j_rand:
                    trial.append(mutant[d])
                else:
                    trial.append(pop[i][d])
            trial_fit = objective(trial)
            if trial_fit <= fitness[i]:
                pop[i] = trial
                fitness[i] = trial_fit
                if trial_fit < best_fit:
                    best = trial[:]
                    best_fit = trial_fit
    return best, best_fit


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    best, val = de_current_to_best(sphere, dim=5, bounds=(-5, 5), generations=40, seed=14)
    assert val < 1.0
    print("de_current_to_best self-tests passed")
