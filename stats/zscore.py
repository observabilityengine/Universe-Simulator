"""Z-score standardization.

Complexity: O(n).
Returns standardized values and optionally mean/std used. Original implementation.
"""
from __future__ import annotations

from typing import List, Sequence, Tuple
import math


def zscore(data: Sequence[float], ddof: int = 0) -> Tuple[List[float], float, float]:
    """Return (z_scores, mean, std). ddof=1 for sample std."""
    n = len(data)
    if n == 0:
        return [], 0.0, 0.0
    mean = sum(data) / n
    if n - ddof <= 0:
        return [0.0] * n, mean, 0.0
    var = sum((x - mean) ** 2 for x in data) / (n - ddof)
    std = math.sqrt(var)
    if std < 1e-15:
        return [0.0] * n, mean, 0.0
    return [(x - mean) / std for x in data], mean, std


if __name__ == "__main__":
    z, m, s = zscore([1.0, 2.0, 3.0, 4.0, 5.0])
    assert abs(m - 3.0) < 1e-12
    assert abs(sum(z)) < 1e-10
    z2, _, s2 = zscore([5.0, 5.0, 5.0])
    assert z2 == [0.0, 0.0, 0.0]
    assert zscore([])[0] == []
    print("zscore self-tests passed")
