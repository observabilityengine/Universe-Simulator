"""Highest Posterior Density and equal-tailed credible intervals."""
from __future__ import annotations
from typing import List, Tuple


def equal_tailed(samples: List[float], alpha: float = 0.05) -> Tuple[float, float]:
    s = sorted(samples)
    n = len(s)
    lo = s[int(alpha / 2 * n)]
    hi = s[int((1 - alpha / 2) * n) - 1]
    return lo, hi


def hpd(samples: List[float], alpha: float = 0.05) -> Tuple[float, float]:
    s = sorted(samples)
    n = len(s)
    k = int((1 - alpha) * n)
    best_width = float("inf")
    best = (s[0], s[-1])
    for i in range(n - k):
        width = s[i + k] - s[i]
        if width < best_width:
            best_width = width
            best = (s[i], s[i + k])
    return best


if __name__ == "__main__":
    import random
    rng = random.Random(0)
    samples = [rng.gauss(0, 1) for _ in range(1000)]
    lo, hi = equal_tailed(samples)
    assert lo < 0 < hi
    print(f"credible_interval [{lo:.2f},{hi:.2f}]")
    print("credible_interval self-tests passed")
