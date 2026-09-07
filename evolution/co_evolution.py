"""Competitive Co-evolution (two populations).

Complexity: O(pop1 * pop2 * gens). Original implementation.
"""
from __future__ import annotations

import random
from typing import Callable, List, Tuple


def co_evolution(
    fitness_fn: Callable[[List[float], List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    pop_size: int = 15,
    generations: int = 30,
    seed: int = 42,
) -> Tuple[List[float], List[float]]:
    """Two populations co-evolve. Returns (best_from_pop1, best_from_pop2)."""
    rng = random.Random(seed)
    lo, hi = bounds
    pop1 = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(pop_size)]
    pop2 = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(pop_size)]

    def evaluate(pop_a, pop_b):
        scores = []
        for a in pop_a:
            s = sum(fitness_fn(a, b) for b in pop_b) / len(pop_b)
            scores.append(s)
        return scores

    for _ in range(generations):
        scores1 = evaluate(pop1, pop2)
        scores2 = evaluate(pop2, pop1)
        new1 = []
        for _ in range(pop_size):
            i1 = max(rng.sample(range(pop_size), 3), key=lambda i: scores1[i])
            i2 = max(rng.sample(range(pop_size), 3), key=lambda i: scores1[i])
            child = [(pop1[i1][d] + pop1[i2][d]) / 2 for d in range(dim)]
            for d in range(dim):
                if rng.random() < 0.2:
                    child[d] += rng.gauss(0, (hi - lo) * 0.1)
                child[d] = max(lo, min(hi, child[d]))
            new1.append(child)
        new2 = []
        for _ in range(pop_size):
            i1 = max(rng.sample(range(pop_size), 3), key=lambda i: scores2[i])
            i2 = max(rng.sample(range(pop_size), 3), key=lambda i: scores2[i])
            child = [(pop2[i1][d] + pop2[i2][d]) / 2 for d in range(dim)]
            for d in range(dim):
                if rng.random() < 0.2:
                    child[d] += rng.gauss(0, (hi - lo) * 0.1)
                child[d] = max(lo, min(hi, child[d]))
            new2.append(child)
        pop1, pop2 = new1, new2

    scores1 = evaluate(pop1, pop2)
    scores2 = evaluate(pop2, pop1)
    best1 = pop1[max(range(pop_size), key=lambda i: scores1[i])]
    best2 = pop2[max(range(pop_size), key=lambda i: scores2[i])]
    return best1, best2


if __name__ == "__main__":
    def fit(a: List[float], b: List[float]) -> float:
        return sum(a) - sum(b)

    b1, b2 = co_evolution(fit, dim=2, bounds=(-2, 2), generations=15, seed=18)
    assert len(b1) == 2 and len(b2) == 2
    print("co_evolution self-tests passed")
