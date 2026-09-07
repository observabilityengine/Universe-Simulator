"""(mu + lambda) Evolution Strategy with self-adaptive step sizes.

Complexity: O((mu+lambda) * dim * gens). Original implementation.
"""
from __future__ import annotations

import math
import random
from typing import Callable, List, Tuple


def evolution_strategy(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    mu: int = 5,
    lambda_: int = 20,
    generations: int = 40,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """(mu + lambda)-ES with isotropic self-adaptive mutation."""
    rng = random.Random(seed)
    lo, hi = bounds
    parents = []
    for _ in range(mu):
        x = [rng.uniform(lo, hi) for _ in range(dim)]
        sigma = [(hi - lo) * 0.1] * dim
        parents.append((x, sigma, objective(x)))

    best_x, best_fit = parents[0][0][:], parents[0][2]
    tau = 1.0 / math.sqrt(2 * dim)
    tau_prime = 1.0 / math.sqrt(2 * math.sqrt(dim))

    for _ in range(generations):
        offspring = []
        for _ in range(lambda_):
            px, psig, _ = rng.choice(parents)
            global_factor = math.exp(tau_prime * rng.gauss(0, 1))
            new_sig = [max(1e-8, s * global_factor * math.exp(tau * rng.gauss(0, 1))) for s in psig]
            new_x = []
            for d in range(dim):
                val = px[d] + new_sig[d] * rng.gauss(0, 1)
                new_x.append(max(lo, min(hi, val)))
            fit = objective(new_x)
            offspring.append((new_x, new_sig, fit))
            if fit < best_fit:
                best_x = new_x[:]
                best_fit = fit
        combined = parents + offspring
        combined.sort(key=lambda t: t[2])
        parents = combined[:mu]
    return best_x, best_fit


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    best, val = evolution_strategy(sphere, dim=4, bounds=(-5, 5), generations=30, seed=0)
    assert val < 1.5
    print("evolution_strategy self-tests passed")
