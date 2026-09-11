"""Posterior predictive draws from posterior samples."""
from __future__ import annotations
import random
from typing import List


def posterior_predictive(posterior_samples: List[float], sigma: float = 1.0, seed: int = 42) -> List[float]:
    rng = random.Random(seed)
    return [rng.gauss(mu, sigma) for mu in posterior_samples]


if __name__ == "__main__":
    post = [0.5, 0.6, 0.4, 0.55]
    pred = posterior_predictive(post)
    assert len(pred) == 4
    print(f"posterior_predictive {pred[0]:.3f}")
    print("posterior_predictive self-tests passed")
