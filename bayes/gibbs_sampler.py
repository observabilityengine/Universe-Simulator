"""Gibbs sampler for bivariate normal."""
from __future__ import annotations
import math
import random
from typing import List, Tuple


def gibbs_bivariate_normal(
    mu: Tuple[float, float] = (0, 0),
    sigma: Tuple[float, float] = (1, 1),
    rho: float = 0.5,
    n_samples: int = 1000,
    seed: int = 42,
) -> List[Tuple[float, float]]:
    rng = random.Random(seed)
    x, y = 0.0, 0.0
    samples = []
    for _ in range(n_samples):
        x = rng.gauss(mu[0] + rho * sigma[0] / sigma[1] * (y - mu[1]), sigma[0] * math.sqrt(1 - rho ** 2))
        y = rng.gauss(mu[1] + rho * sigma[1] / sigma[0] * (x - mu[0]), sigma[1] * math.sqrt(1 - rho ** 2))
        samples.append((x, y))
    return samples


if __name__ == "__main__":
    samples = gibbs_bivariate_normal(n_samples=2000)
    mean_x = sum(s[0] for s in samples[500:]) / len(samples[500:])
    assert abs(mean_x) < 0.3
    print(f"gibbs_sampler mean_x={mean_x:.3f}")
    print("gibbs_sampler self-tests passed")
