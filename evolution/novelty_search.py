"""Novelty Search (archive-based behavioral diversity).

Complexity: O(pop * archive * gens). Original implementation.
"""
from __future__ import annotations

import math
import random
from typing import Callable, List, Tuple


def novelty_search(
    behavior: Callable[[List[float]], List[float]],
    dim: int,
    bounds: Tuple[float, float],
    pop_size: int = 20,
    generations: int = 30,
    k_nearest: int = 5,
    archive_prob: float = 0.1,
    seed: int = 42,
) -> List[List[float]]:
    """Novelty search. Returns final population (diverse behaviors)."""
    rng = random.Random(seed)
    lo, hi = bounds
    pop = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(pop_size)]
    archive: List[List[float]] = []

    def dist(a: List[float], b: List[float]) -> float:
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

    def novelty(b: List[float], archive_and_pop: List[List[float]]) -> float:
        if not archive_and_pop:
            return 0.0
        dists = sorted(dist(b, other) for other in archive_and_pop)
        k = min(k_nearest, len(dists))
        return sum(dists[:k]) / k

    for _ in range(generations):
        behaviors = [behavior(ind) for ind in pop]
        all_beh = archive + behaviors
        novelties = [novelty(b, all_beh) for b in behaviors]
        order = sorted(range(pop_size), key=lambda i: novelties[i], reverse=True)
        new_pop = []
        for i in range(pop_size):
            parent = pop[order[i % (pop_size // 2 + 1)]]
            child = parent[:]
            for d in range(dim):
                if rng.random() < 0.3:
                    child[d] += rng.gauss(0, (hi - lo) * 0.1)
                child[d] = max(lo, min(hi, child[d]))
            new_pop.append(child)
        for i, b in enumerate(behaviors):
            if rng.random() < archive_prob:
                archive.append(b)
        pop = new_pop
    return pop


if __name__ == "__main__":
    def beh(x: List[float]) -> List[float]:
        return x[:]

    pop = novelty_search(beh, dim=2, bounds=(-5, 5), generations=15, seed=10)
    assert len(pop) == 20
    assert all(len(ind) == 2 for ind in pop)
    print("novelty_search self-tests passed")
