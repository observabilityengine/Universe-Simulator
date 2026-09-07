"""SPEA2 (Strength Pareto Evolutionary Algorithm 2) - simplified.

Complexity: O(pop^2 * gens). Original bi-objective implementation.
"""
from __future__ import annotations

import random
from typing import Callable, List, Tuple


def spea2(
    objectives: List[Callable[[List[float]], float]],
    dim: int,
    bounds: Tuple[float, float],
    pop_size: int = 25,
    archive_size: int = 20,
    generations: int = 30,
    seed: int = 42,
) -> List[Tuple[List[float], List[float]]]:
    """Return archive of non-dominated solutions."""
    rng = random.Random(seed)
    lo, hi = bounds
    pop = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(pop_size)]
    archive: List[List[float]] = []

    def evaluate(ind: List[float]) -> List[float]:
        return [obj(ind) for obj in objectives]

    def dominates(f1: List[float], f2: List[float]) -> bool:
        return all(a <= b for a, b in zip(f1, f2)) and any(a < b for a, b in zip(f1, f2))

    for _ in range(generations):
        combined = pop + archive
        fits = [evaluate(ind) for ind in combined]
        n = len(combined)
        strength = [0] * n
        for i in range(n):
            for j in range(n):
                if dominates(fits[i], fits[j]):
                    strength[i] += 1
        raw = [0.0] * n
        for i in range(n):
            for j in range(n):
                if dominates(fits[j], fits[i]):
                    raw[i] += strength[j]
        k = int(n ** 0.5)
        density = []
        for i in range(n):
            dists = sorted(
                sum((fits[i][m] - fits[j][m]) ** 2 for m in range(len(fits[0]))) ** 0.5
                for j in range(n) if j != i
            )
            dens = 1.0 / (dists[min(k, len(dists) - 1)] + 2.0) if dists else 0.0
            density.append(dens)
        fitness = [raw[i] + density[i] for i in range(n)]
        nondom = [i for i in range(n) if raw[i] == 0]
        if len(nondom) <= archive_size:
            order = sorted(range(n), key=lambda i: fitness[i])
            archive = [combined[i] for i in order[:archive_size]]
        else:
            archive = [combined[i] for i in nondom[:archive_size]]
        pop = []
        for _ in range(pop_size):
            if len(archive) >= 2:
                p1, p2 = rng.sample(archive, 2)
            else:
                p1 = p2 = archive[0] if archive else [rng.uniform(lo, hi) for _ in range(dim)]
            child = [(p1[d] + p2[d]) / 2 for d in range(dim)]
            for d in range(dim):
                if rng.random() < 0.2:
                    child[d] += rng.gauss(0, (hi - lo) * 0.1)
                child[d] = max(lo, min(hi, child[d]))
            pop.append(child)
    result = [(ind, evaluate(ind)) for ind in archive]
    return result


if __name__ == "__main__":
    def f1(x: List[float]) -> float:
        return sum(v * v for v in x)

    def f2(x: List[float]) -> float:
        return sum((v - 1) ** 2 for v in x)

    front = spea2([f1, f2], dim=2, bounds=(-2, 2), generations=15, seed=13)
    assert len(front) >= 1
    print("spea2 self-tests passed")
