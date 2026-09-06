"""Monte Carlo estimation of pi via unit square / quarter circle.

Complexity: O(n) samples.
Returns estimate; error ~ 1/sqrt(n).
"""
from __future__ import annotations

import random


def monte_carlo_pi(n: int, seed: int | None = None) -> float:
    """Estimate pi with n uniform samples in [0,1)^2."""
    if n < 1:
        raise ValueError("n >= 1")
    rng = random.Random(seed)
    inside = 0
    for _ in range(n):
        x = rng.random()
        y = rng.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return 4.0 * inside / n


if __name__ == "__main__":
    est = monte_carlo_pi(100000, seed=42)
    assert abs(est - 3.14159) < 0.02
    est2 = monte_carlo_pi(1, seed=0)
    assert 0.0 <= est2 <= 4.0
    try:
        monte_carlo_pi(0)
        assert False
    except ValueError:
        pass
    print("monte_carlo_pi self-tests passed")
