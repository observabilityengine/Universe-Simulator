"""Simplified NUTS-inspired adaptive trajectory HMC."""
from __future__ import annotations
import math
import random
from typing import Callable, List
from .hamiltonian_mcmc import hmc


def nuts_simple(
    log_prob: Callable[[float], float],
    grad_log_prob: Callable[[float], float],
    x0: float,
    n_samples: int = 400,
    step_size: float = 0.1,
    max_tree_depth: int = 4,
    seed: int = 42,
) -> List[float]:
    """Uses doubling trajectory length as a NUTS-like heuristic."""
    rng = random.Random(seed)
    x = x0
    samples = []
    for i in range(n_samples):
        depth = min(max_tree_depth, 1 + i // 50)
        n_leap = 2 ** depth
        batch = hmc(log_prob, grad_log_prob, x, 1, step_size, n_leap, seed + i)
        x = batch[0]
        samples.append(x)
    return samples


if __name__ == "__main__":
    def logp(x):
        return -0.5 * x * x
    def grad(x):
        return -x
    samples = nuts_simple(logp, grad, 0.0, 300)
    mean = sum(samples[100:]) / len(samples[100:])
    assert abs(mean) < 0.5
    print(f"nuts mean={mean:.3f}")
    print("nuts self-tests passed")
