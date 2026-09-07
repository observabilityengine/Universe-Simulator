"""NSGA-II (Non-dominated Sorting Genetic Algorithm II) - simplified bi-objective.

Complexity: O(pop^2 * gens). Original implementation for 2 objectives.
"""
from __future__ import annotations

import random
from typing import Callable, List, Tuple


def nsga2(
    objectives: List[Callable[[List[float]], float]],
    dim: int,
    bounds: Tuple[float, float],
    pop_size: int = 30,
    generations: int = 40,
    seed: int = 42,
) -> List[Tuple[List[float], List[float]]]:
    """Return approximate Pareto front as list of (x, [f1, f2, ...])."""
    assert len(objectives) >= 2
    rng = random.Random(seed)
    lo, hi = bounds
    pop = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(pop_size)]

    def evaluate(ind: List[float]) -> List[float]:
        return [obj(ind) for obj in objectives]

    def dominates(f1: List[float], f2: List[float]) -> bool:
        return all(a <= b for a, b in zip(f1, f2)) and any(a < b for a, b in zip(f1, f2))

    def non_dominated_sort(fits: List[List[float]]) -> List[List[int]]:
        n = len(fits)
        fronts: List[List[int]] = [[]]
        domination_count = [0] * n
        dominated = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if dominates(fits[i], fits[j]):
                    dominated[i].append(j)
                elif dominates(fits[j], fits[i]):
                    domination_count[i] += 1
            if domination_count[i] == 0:
                fronts[0].append(i)
        i = 0
        while fronts[i]:
            next_front = []
            for p in fronts[i]:
                for q in dominated[p]:
                    domination_count[q] -= 1
                    if domination_count[q] == 0:
                        next_front.append(q)
            i += 1
            fronts.append(next_front)
        return fronts[:-1]

    def crowding_distance(front: List[int], fits: List[List[float]]) -> List[float]:
        n = len(front)
        if n == 0:
            return []
        dist = [0.0] * n
        m = len(fits[0])
        for obj_idx in range(m):
            sorted_idx = sorted(range(n), key=lambda k: fits[front[k]][obj_idx])
            dist[sorted_idx[0]] = float("inf")
            dist[sorted_idx[-1]] = float("inf")
            fmin = fits[front[sorted_idx[0]]][obj_idx]
            fmax = fits[front[sorted_idx[-1]]][obj_idx]
            if fmax == fmin:
                continue
            for k in range(1, n - 1):
                dist[sorted_idx[k]] += (fits[front[sorted_idx[k + 1]]][obj_idx] - fits[front[sorted_idx[k - 1]]][obj_idx]) / (fmax - fmin)
        return dist

    fits = [evaluate(ind) for ind in pop]
    for _ in range(generations):
        offspring = []
        while len(offspring) < pop_size:
            i, j = rng.sample(range(pop_size), 2)
            child = [(pop[i][d] + pop[j][d]) / 2 for d in range(dim)]
            for d in range(dim):
                if rng.random() < 0.2:
                    child[d] += rng.gauss(0, (hi - lo) * 0.1)
                child[d] = max(lo, min(hi, child[d]))
            offspring.append(child)
        combined = pop + offspring
        combined_fits = fits + [evaluate(ind) for ind in offspring]
        fronts = non_dominated_sort(combined_fits)
        new_pop = []
        new_fits = []
        for front in fronts:
            if len(new_pop) + len(front) <= pop_size:
                for idx in front:
                    new_pop.append(combined[idx])
                    new_fits.append(combined_fits[idx])
            else:
                dist = crowding_distance(front, combined_fits)
                ranked = sorted(range(len(front)), key=lambda k: dist[k], reverse=True)
                for k in ranked:
                    if len(new_pop) >= pop_size:
                        break
                    idx = front[k]
                    new_pop.append(combined[idx])
                    new_fits.append(combined_fits[idx])
                break
        pop = new_pop
        fits = new_fits

    fronts = non_dominated_sort(fits)
    result = [(pop[i], fits[i]) for i in fronts[0]]
    return result


if __name__ == "__main__":
    def f1(x: List[float]) -> float:
        return sum(v * v for v in x)

    def f2(x: List[float]) -> float:
        return sum((v - 1) ** 2 for v in x)

    front = nsga2([f1, f2], dim=2, bounds=(-2, 2), pop_size=20, generations=15, seed=6)
    assert len(front) >= 1
    assert all(len(f) == 2 for _, f in front)
    print("nsga2 self-tests passed")
