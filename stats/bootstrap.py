"""Bootstrap resampling for confidence intervals.

Complexity: O(n_boot * n). Original implementation.
"""
from __future__ import annotations
import random
from typing import Callable, List, Tuple

def bootstrap_ci(
    data: List[float],
    statistic: Callable[[List[float]], float] = lambda xs: sum(xs)/len(xs),
    n_boot: int = 1000,
    alpha: float = 0.05,
    seed: int = 42,
) -> Tuple[float, float, float]:
    rng = random.Random(seed)
    n = len(data)
    point = statistic(data)
    boots = []
    for _ in range(n_boot):
        sample = [data[rng.randrange(n)] for _ in range(n)]
        boots.append(statistic(sample))
    boots.sort()
    lo = boots[int(alpha/2 * n_boot)]
    hi = boots[int((1-alpha/2) * n_boot)]
    return point, lo, hi

if __name__ == "__main__":
    data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    mean, lo, hi = bootstrap_ci(data, n_boot=500, seed=1)
    assert abs(mean - 5.5) < 1e-9
    assert lo < mean < hi
    print("bootstrap self-tests passed")
