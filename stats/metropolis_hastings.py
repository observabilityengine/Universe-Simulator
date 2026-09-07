"""Metropolis-Hastings MCMC sampler.

Complexity: O(samples * cost(target)). Original implementation.
"""
from __future__ import annotations
import math
import random
from typing import Callable, List

def metropolis_hastings(
    log_target: Callable[[List[float]], float],
    dim: int,
    n_samples: int = 5000,
    proposal_scale: float = 0.5,
    burn_in: int = 1000,
    seed: int = 42,
    init: List[float] | None = None,
) -> List[List[float]]:
    rng = random.Random(seed)
    if init is None:
        current = [rng.gauss(0, 1) for _ in range(dim)]
    else:
        current = init[:]
    current_logp = log_target(current)
    samples: List[List[float]] = []
    for i in range(n_samples + burn_in):
        proposal = [current[d] + rng.gauss(0, proposal_scale) for d in range(dim)]
        prop_logp = log_target(proposal)
        log_alpha = prop_logp - current_logp
        if log_alpha > 0 or rng.random() < math.exp(log_alpha):
            current = proposal
            current_logp = prop_logp
        if i >= burn_in:
            samples.append(current[:])
    return samples

if __name__ == "__main__":
    def log_std_normal(x: List[float]) -> float:
        return -0.5 * sum(v * v for v in x)
    samples = metropolis_hastings(log_std_normal, dim=2, n_samples=3000, burn_in=500, proposal_scale=0.8, seed=1)
    assert len(samples) == 3000
    mean0 = sum(s[0] for s in samples) / len(samples)
    mean1 = sum(s[1] for s in samples) / len(samples)
    assert abs(mean0) < 0.15
    assert abs(mean1) < 0.15
    var0 = sum((s[0] - mean0) ** 2 for s in samples) / len(samples)
    assert 0.7 < var0 < 1.4
    print("metropolis_hastings self-tests passed")
