"""Simulated Annealing continuous optimizer.

Complexity: O(iters * cost(f)). Original implementation.
"""
from __future__ import annotations
import math
import random
from typing import Callable, List, Tuple

def simulated_annealing(
    objective: Callable[[List[float]], float],
    bounds: List[Tuple[float, float]],
    n_iter: int = 5000,
    t0: float = 10.0,
    t_min: float = 1e-8,
    cooling: float = 0.995,
    seed: int = 42,
) -> Tuple[List[float], float]:
    rng = random.Random(seed)
    dim = len(bounds)
    x = [rng.uniform(lo, hi) for lo, hi in bounds]
    fx = objective(x)
    best, best_f = x[:], fx
    T = t0
    for _ in range(n_iter):
        i = rng.randrange(dim)
        lo, hi = bounds[i]
        step = (hi - lo) * 0.1 * T / t0
        cand = x[:]
        cand[i] = max(lo, min(hi, x[i] + rng.gauss(0, step + 1e-12)))
        fc = objective(cand)
        dE = fc - fx
        if dE < 0 or rng.random() < math.exp(-dE / max(T, 1e-15)):
            x, fx = cand, fc
            if fx < best_f:
                best, best_f = x[:], fx
        T = max(t_min, T * cooling)
    return best, best_f

if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)
    best, val = simulated_annealing(sphere, [(-5, 5)] * 3, n_iter=3000, t0=5.0, seed=1)
    assert val < 0.5, val
    assert all(abs(v) < 1.0 for v in best)
    print("simulated_annealing self-tests passed")
