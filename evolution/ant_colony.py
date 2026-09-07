"""Ant Colony Optimization for continuous domains (ACOR-style).

Complexity: O(ants * dim * iters). Original implementation.
"""
from __future__ import annotations

import math
import random
from typing import Callable, List, Tuple


def ant_colony(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    n_ants: int = 20,
    iterations: int = 40,
    q: float = 0.1,
    xi: float = 0.85,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """Continuous ACO (archive-based)."""
    rng = random.Random(seed)
    lo, hi = bounds
    archive_size = n_ants
    archive = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(archive_size)]
    fitness = [objective(a) for a in archive]
    order = sorted(range(archive_size), key=lambda i: fitness[i])
    archive = [archive[i] for i in order]
    fitness = [fitness[i] for i in order]
    best = archive[0][:]
    best_fit = fitness[0]

    for _ in range(iterations):
        new_sols = []
        for _ in range(n_ants):
            weights = [1.0 / (q * archive_size * math.sqrt(2 * math.pi)) * math.exp(-0.5 * ((k) / (q * archive_size)) ** 2) for k in range(archive_size)]
            wsum = sum(weights)
            weights = [w / wsum for w in weights]
            r = rng.random()
            cum = 0.0
            guide_idx = 0
            for k, w in enumerate(weights):
                cum += w
                if r <= cum:
                    guide_idx = k
                    break
            guide = archive[guide_idx]
            sol = []
            for d in range(dim):
                mean = guide[d]
                sigma = xi * sum(abs(archive[k][d] - guide[d]) for k in range(archive_size)) / (archive_size - 1 + 1e-12)
                val = rng.gauss(mean, max(sigma, 1e-8))
                sol.append(max(lo, min(hi, val)))
            new_sols.append(sol)
        for sol in new_sols:
            fit = objective(sol)
            if fit < fitness[-1]:
                pos = archive_size - 1
                while pos > 0 and fit < fitness[pos - 1]:
                    pos -= 1
                archive.insert(pos, sol)
                fitness.insert(pos, fit)
                archive.pop()
                fitness.pop()
                if fit < best_fit:
                    best = sol[:]
                    best_fit = fit
    return best, best_fit


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    best, val = ant_colony(sphere, dim=3, bounds=(-5, 5), iterations=25, seed=4)
    assert val < 3.0
    print("ant_colony self-tests passed")
