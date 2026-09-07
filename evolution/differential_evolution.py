"""Differential Evolution (DE/rand/1/bin).

Complexity: O(pop * dim * gens). Original implementation.
"""
from __future__ import annotations

import random
from typing import Callable, List, Tuple


def differential_evolution(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    pop_size: int = 20,
    generations: int = 50,
    F: float = 0.8,
    CR: float = 0.9,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """Minimize objective with classic DE/rand/1/bin."""
    rng = random.Random(seed)
    lo, hi = bounds
    pop = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(pop_size)]
    fitness = [objective(ind) for ind in pop]
    best_idx = min(range(pop_size), key=lambda i: fitness[i])
    best = pop[best_idx][:]
    best_fit = fitness[best_idx]

    for _ in range(generations):
        for i in range(pop_size):
            idxs = list(range(pop_size))
            idxs.remove(i)
            a, b, c = rng.sample(idxs, 3)
            mutant = []
            for d in range(dim):
                val = pop[a][d] + F * (pop[b][d] - pop[c][d])
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

    best, val = differential_evolution(sphere, dim=5, bounds=(-5, 5), generations=40, seed=1)
    assert val < 1.0
    assert len(best) == 5
    print("differential_evolution self-tests passed")
