"""Island Model Genetic Algorithm with migration.

Complexity: O(islands * pop * dim * gens). Original implementation.
"""
from __future__ import annotations

import random
from typing import Callable, List, Tuple


def island_ga(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    n_islands: int = 4,
    pop_per_island: int = 15,
    generations: int = 30,
    migration_interval: int = 5,
    migration_size: int = 2,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """Multi-island GA with ring migration."""
    rng = random.Random(seed)
    lo, hi = bounds
    islands = []
    for _ in range(n_islands):
        pop = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(pop_per_island)]
        fits = [objective(ind) for ind in pop]
        islands.append((pop, fits))

    best = islands[0][0][0][:]
    best_fit = islands[0][1][0]

    def tournament(pop, fits, k=3):
        idxs = rng.sample(range(len(pop)), k)
        return min(idxs, key=lambda i: fits[i])

    for gen in range(generations):
        for isl in range(n_islands):
            pop, fits = islands[isl]
            new_pop = []
            new_fits = []
            for _ in range(pop_per_island):
                i1 = tournament(pop, fits)
                i2 = tournament(pop, fits)
                child = [(pop[i1][d] + pop[i2][d]) / 2 for d in range(dim)]
                for d in range(dim):
                    if rng.random() < 0.15:
                        child[d] += rng.gauss(0, (hi - lo) * 0.08)
                    child[d] = max(lo, min(hi, child[d]))
                fit = objective(child)
                new_pop.append(child)
                new_fits.append(fit)
                if fit < best_fit:
                    best = child[:]
                    best_fit = fit
            islands[isl] = (new_pop, new_fits)

        if (gen + 1) % migration_interval == 0:
            for isl in range(n_islands):
                next_isl = (isl + 1) % n_islands
                pop_a, fits_a = islands[isl]
                pop_b, fits_b = islands[next_isl]
                order_a = sorted(range(len(pop_a)), key=lambda i: fits_a[i])
                for m in range(migration_size):
                    order_b = sorted(range(len(pop_b)), key=lambda i: fits_b[i], reverse=True)
                    worst = order_b[m]
                    src = order_a[m]
                    pop_b[worst] = pop_a[src][:]
                    fits_b[worst] = fits_a[src]
                islands[next_isl] = (pop_b, fits_b)

    return best, best_fit


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    best, val = island_ga(sphere, dim=3, bounds=(-5, 5), generations=20, seed=7)
    assert val < 2.0
    print("island_ga self-tests passed")
