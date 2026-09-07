"""MAP-Elites (illumination algorithm).

Complexity: O(evals * grid). Original simple grid implementation.
"""
from __future__ import annotations

import random
from typing import Callable, Dict, List, Tuple


def map_elites(
    objective: Callable[[List[float]], float],
    behavior: Callable[[List[float]], Tuple[float, float]],
    dim: int,
    bounds: Tuple[float, float],
    n_bins: int = 10,
    evaluations: int = 500,
    seed: int = 42,
) -> Dict[Tuple[int, int], Tuple[List[float], float]]:
    """Simple 2D MAP-Elites. Returns archive: (bin_x, bin_y) -> (solution, fitness)."""
    rng = random.Random(seed)
    lo, hi = bounds
    archive: Dict[Tuple[int, int], Tuple[List[float], float]] = {}

    def to_bin(b: Tuple[float, float]) -> Tuple[int, int]:
        bx = int((b[0] - lo) / (hi - lo + 1e-12) * n_bins)
        by = int((b[1] - lo) / (hi - lo + 1e-12) * n_bins)
        bx = max(0, min(n_bins - 1, bx))
        by = max(0, min(n_bins - 1, by))
        return bx, by

    for _ in range(max(20, n_bins)):
        x = [rng.uniform(lo, hi) for _ in range(dim)]
        fit = objective(x)
        b = behavior(x)
        key = to_bin(b)
        if key not in archive or fit < archive[key][1]:
            archive[key] = (x[:], fit)

    for _ in range(evaluations):
        if not archive:
            break
        key = rng.choice(list(archive.keys()))
        parent = archive[key][0]
        child = parent[:]
        for d in range(dim):
            if rng.random() < 0.5:
                child[d] += rng.gauss(0, (hi - lo) * 0.1)
            child[d] = max(lo, min(hi, child[d]))
        fit = objective(child)
        b = behavior(child)
        ckey = to_bin(b)
        if ckey not in archive or fit < archive[ckey][1]:
            archive[ckey] = (child, fit)
    return archive


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    def beh(x: List[float]) -> Tuple[float, float]:
        return (x[0], x[1] if len(x) > 1 else 0.0)

    archive = map_elites(sphere, beh, dim=2, bounds=(-5, 5), n_bins=5, evaluations=100, seed=11)
    assert len(archive) >= 1
    print("map_elites self-tests passed", len(archive), "cells filled")
