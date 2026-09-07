"""Adaptive Differential Evolution (jDE-style self-adaptive F and CR).

Complexity: O(pop * dim * gens). Original implementation.
"""
from __future__ import annotations

import random
from typing import Callable, List, Tuple


def adaptive_de(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    pop_size: int = 20,
    generations: int = 50,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """jDE: each individual carries its own F and CR that adapt."""
    rng = random.Random(seed)
    lo, hi = bounds
    pop = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(pop_size)]
    fitness = [objective(ind) for ind in pop]
    F = [rng.uniform(0.1, 1.0) for _ in range(pop_size)]
    CR = [rng.uniform(0.0, 1.0) for _ in range(pop_size)]
    best_idx = min(range(pop_size), key=lambda i: fitness[i])
    best = pop[best_idx][:]
    best_fit = fitness[best_idx]

    tau1, tau2 = 0.1, 0.1  # probability to adjust F / CR

    for _ in range(generations):
        for i in range(pop_size):
            # Adapt parameters
            Fi = F[i]
            CRi = CR[i]
            if rng.random() < tau1:
                Fi = 0.1 + rng.random() * 0.9
            if rng.random() < tau2:
                CRi = rng.random()
            # Mutation
            idxs = [j for j in range(pop_size) if j != i]
            a, b, c = rng.sample(idxs, 3)
            mutant = []
            for d in range(dim):
                val = pop[a][d] + Fi * (pop[b][d] - pop[c][d])
                mutant.append(max(lo, min(hi, val)))
            # Crossover
            trial = []
            j_rand = rng.randrange(dim)
            for d in range(dim):
                if rng.random() < CRi or d == j_rand:
                    trial.append(mutant[d])
                else:
                    trial.append(pop[i][d])
            trial_fit = objective(trial)
            if trial_fit <= fitness[i]:
                pop[i] = trial
                fitness[i] = trial_fit
                F[i] = Fi
                CR[i] = CRi
                if trial_fit < best_fit:
                    best = trial[:]
                    best_fit = trial_fit
    return best, best_fit


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    best, val = adaptive_de(sphere, dim=5, bounds=(-5, 5), generations=40, seed=17)
    assert val < 1.0
    print("adaptive_de self-tests passed")
