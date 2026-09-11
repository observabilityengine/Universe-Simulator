"""Prior predictive draws."""
from __future__ import annotations
import random
from typing import List


def prior_predictive_normal(mu0: float, sigma0: float, sigma: float, n_draws: int = 100, seed: int = 42) -> List[float]:
    rng = random.Random(seed)
    return [rng.gauss(rng.gauss(mu0, sigma0), sigma) for _ in range(n_draws)]


if __name__ == "__main__":
    draws = prior_predictive_normal(0, 1, 1, 50)
    assert len(draws) == 50
    print(f"prior_predictive mean={sum(draws)/len(draws):.3f}")
    print("prior_predictive self-tests passed")
