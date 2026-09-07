"""Grey Wolf Optimizer (GWO).

Complexity: O(pop * dim * iters). Original implementation.
"""
from __future__ import annotations

import random
from typing import Callable, List, Tuple


def grey_wolf(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    n_wolves: int = 20,
    iterations: int = 50,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """Minimize with Grey Wolf Optimizer."""
    rng = random.Random(seed)
    lo, hi = bounds
    wolves = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(n_wolves)]
    fitness = [objective(w) for w in wolves]

    order = sorted(range(n_wolves), key=lambda i: fitness[i])
    alpha = wolves[order[0]][:]
    beta = wolves[order[1]][:]
    delta = wolves[order[2]][:]
    alpha_fit = fitness[order[0]]

    for t in range(iterations):
        a = 2.0 - 2.0 * t / iterations
        for i in range(n_wolves):
            for d in range(dim):
                r1, r2 = rng.random(), rng.random()
                A1 = 2 * a * r1 - a
                C1 = 2 * r2
                D_alpha = abs(C1 * alpha[d] - wolves[i][d])
                X1 = alpha[d] - A1 * D_alpha

                r1, r2 = rng.random(), rng.random()
                A2 = 2 * a * r1 - a
                C2 = 2 * r2
                D_beta = abs(C2 * beta[d] - wolves[i][d])
                X2 = beta[d] - A2 * D_beta

                r1, r2 = rng.random(), rng.random()
                A3 = 2 * a * r1 - a
                C3 = 2 * r2
                D_delta = abs(C3 * delta[d] - wolves[i][d])
                X3 = delta[d] - A3 * D_delta

                wolves[i][d] = max(lo, min(hi, (X1 + X2 + X3) / 3.0))
            fitness[i] = objective(wolves[i])

        order = sorted(range(n_wolves), key=lambda i: fitness[i])
        if fitness[order[0]] < alpha_fit:
            alpha = wolves[order[0]][:]
            alpha_fit = fitness[order[0]]
        beta = wolves[order[1]][:]
        delta = wolves[order[2]][:]

    return alpha, alpha_fit


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    best, val = grey_wolf(sphere, dim=4, bounds=(-5, 5), iterations=40, seed=1)
    assert val < 1.0
    print("grey_wolf self-tests passed")
