"""Stochastic Ranking for constrained evolutionary optimization.

Complexity: O(pop * gens * bubble). Original implementation.
"""
from __future__ import annotations

import random
from typing import Callable, List, Tuple


def stochastic_ranking(
    objective: Callable[[List[float]], float],
    constraints: List[Callable[[List[float]], float]],
    dim: int,
    bounds: Tuple[float, float],
    pop_size: int = 30,
    generations: int = 40,
    pf: float = 0.45,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """Minimize objective subject to constraints(c) <= 0 using stochastic ranking."""
    rng = random.Random(seed)
    lo, hi = bounds
    pop = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(pop_size)]

    def phi(ind: List[float]) -> float:
        return sum(max(0.0, c(ind)) for c in constraints)

    fitness = [objective(ind) for ind in pop]
    viol = [phi(ind) for ind in pop]

    best = pop[0][:]
    best_fit = float("inf")

    for _ in range(generations):
        for _ in range(pop_size):
            swapped = False
            for i in range(pop_size - 1):
                u = rng.random()
                if (viol[i] == 0 and viol[i + 1] == 0) or u < pf:
                    if fitness[i] > fitness[i + 1]:
                        pop[i], pop[i + 1] = pop[i + 1], pop[i]
                        fitness[i], fitness[i + 1] = fitness[i + 1], fitness[i]
                        viol[i], viol[i + 1] = viol[i + 1], viol[i]
                        swapped = True
                else:
                    if viol[i] > viol[i + 1]:
                        pop[i], pop[i + 1] = pop[i + 1], pop[i]
                        fitness[i], fitness[i + 1] = fitness[i + 1], fitness[i]
                        viol[i], viol[i + 1] = viol[i + 1], viol[i]
                        swapped = True
            if not swapped:
                break

        for i in range(pop_size):
            if viol[i] == 0 and fitness[i] < best_fit:
                best = pop[i][:]
                best_fit = fitness[i]

        new_pop = pop[: pop_size // 2]
        while len(new_pop) < pop_size:
            p1, p2 = rng.sample(pop[: pop_size // 2], 2)
            child = [(p1[d] + p2[d]) / 2 for d in range(dim)]
            for d in range(dim):
                if rng.random() < 0.2:
                    child[d] += rng.gauss(0, (hi - lo) * 0.1)
                child[d] = max(lo, min(hi, child[d]))
            new_pop.append(child)
        pop = new_pop
        fitness = [objective(ind) for ind in pop]
        viol = [phi(ind) for ind in pop]

    if best_fit == float("inf"):
        idx = min(range(pop_size), key=lambda i: (viol[i], fitness[i]))
        return pop[idx], fitness[idx]
    return best, best_fit


if __name__ == "__main__":
    def obj(x: List[float]) -> float:
        return sum(v * v for v in x)

    def c1(x: List[float]) -> float:
        return sum(x) - 1.0

    best, val = stochastic_ranking(obj, [c1], dim=3, bounds=(-2, 2), generations=25, seed=16)
    assert sum(best) <= 1.5
    print("stochastic_ranking self-tests passed")
