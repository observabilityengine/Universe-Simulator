"""
Module 69 – Bootstrap Resampling
Estimate standard error and confidence intervals via bootstrap.
Complete implementation.
"""

from __future__ import annotations
import random
import math
from typing import Callable, List, Tuple, Any


def bootstrap(
    data: List[Any],
    statistic: Callable[[List[Any]], float],
    n_resamples: int = 1000,
    seed: int | None = None,
) -> Tuple[float, float, Tuple[float, float]]:
    rng = random.Random(seed)
    n = len(data)
    point = statistic(data)
    samples = []
    for _ in range(n_resamples):
        resample = [data[rng.randrange(n)] for _ in range(n)]
        samples.append(statistic(resample))
    samples.sort()
    se = math.sqrt(sum((x - point) ** 2 for x in samples) / (n_resamples - 1))
    lo = samples[int(0.025 * n_resamples)]
    hi = samples[int(0.975 * n_resamples)]
    return point, se, (lo, hi)


if __name__ == "__main__":
    print("Testing Bootstrap...")
    data = [2.1, 2.3, 1.8, 2.0, 2.5, 1.9, 2.2, 2.4, 2.0, 1.7]
    mean_est, se, (lo, hi) = bootstrap(data, lambda xs: sum(xs) / len(xs), n_resamples=2000, seed=42)
    print(f"  Mean: {mean_est:.3f}  SE: {se:.3f}  95% CI: [{lo:.3f}, {hi:.3f}]")
    med_est, se_m, ci_m = bootstrap(data, lambda xs: sorted(xs)[len(xs)//2], n_resamples=2000, seed=1)
    print(f"  Median: {med_est:.3f}  SE: {se_m:.3f}  95% CI: [{ci_m[0]:.3f}, {ci_m[1]:.3f}]")
    print("Bootstrap module OK.")
