"""Whale Optimization Algorithm (WOA).

Complexity: O(pop * dim * iters). Original implementation.
"""
from __future__ import annotations

import math
import random
from typing import Callable, List, Tuple


def whale_opt(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    n_whales: int = 20,
    iterations: int = 50,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """Minimize with Whale Optimization Algorithm."""
    rng = random.Random(seed)
    lo, hi = bounds
    pop = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(n_whales)]
    fitness = [objective(p) for p in pop]
    best_idx = min(range(n_whales), key=lambda i: fitness[i])
    best = pop[best_idx][:]
    best_fit = fitness[best_idx]

    for t in range(iterations):
        a = 2.0 - 2.0 * t / iterations
        a2 = -1.0 + t * (-1.0 / iterations)
        for i in range(n_whales):
            r1, r2 = rng.random(), rng.random()
            A = 2 * a * r1 - a
            C = 2 * r2
            b = 1.0
            l = (a2 - 1) * rng.random() + 1
            p = rng.random()

            for d in range(dim):
                if p < 0.5:
                    if abs(A) < 1:
                        D = abs(C * best[d] - pop[i][d])
                        pop[i][d] = best[d] - A * D
                    else:
                        rand_idx = rng.randrange(n_whales)
                        D = abs(C * pop[rand_idx][d] - pop[i][d])
                        pop[i][d] = pop[rand_idx][d] - A * D
                else:
                    D = abs(best[d] - pop[i][d])
                    pop[i][d] = D * math.exp(b * l) * math.cos(2 * math.pi * l) + best[d]
                pop[i][d] = max(lo, min(hi, pop[i][d]))
            fitness[i] = objective(pop[i])
            if fitness[i] < best_fit:
                best = pop[i][:]
                best_fit = fitness[i]
    return best, best_fit


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    best, val = whale_opt(sphere, dim=4, bounds=(-5, 5), iterations=40, seed=3)
    assert val < 1.5
    print("whale_opt self-tests passed")
