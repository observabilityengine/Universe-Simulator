"""Metropolis-Hastings MCMC sampler."""
from __future__ import annotations
import math
import random
from typing import Callable, List


def metropolis_hastings(
    log_prob: Callable[[float], float],
    x0: float,
    n_samples: int = 1000,
    step: float = 0.5,
    seed: int = 42,
) -> List[float]:
    rng = random.Random(seed)
    x = x0
    samples = []
    for _ in range(n_samples):
        prop = x + rng.gauss(0, step)
        log_alpha = log_prob(prop) - log_prob(x)
        if math.log(rng.random()) < log_alpha:
            x = prop
        samples.append(x)
    return samples


if __name__ == "__main__":
    def log_std_normal(x):
        return -0.5 * x * x
    samples = metropolis_hastings(log_std_normal, 0.0, 2000, 0.8)
    mean = sum(samples[500:]) / len(samples[500:])
    assert abs(mean) < 0.3
    print(f"metropolis_hastings mean={mean:.3f}")
    print("metropolis_hastings self-tests passed")
