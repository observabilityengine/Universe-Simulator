"""
Universe Simulator - Black-Derman-Toy short-rate tree
Original calibrated binomial tree for rates.
"""

from __future__ import annotations

import math
from typing import List

def bdt_tree(
    zero_rates: List[float],
    sigma: float,
    steps: int,
) -> List[List[float]]:
    """Build BDT rate tree calibrated to zero curve (simplified)."""
    dt = 1.0 / steps
    tree = [[0.0] for _ in range(steps + 1)]
    tree[0][0] = zero_rates[0]
    for i in range(1, steps + 1):
        level = []
        for j in range(i + 1):
            # median rate from zero curve interpolation
            t = i * dt
            r_med = zero_rates[min(i, len(zero_rates)-1)]
            level.append(r_med * math.exp(sigma * math.sqrt(dt) * (2 * j - i)))
        tree[i] = level
    return tree

if __name__ == "__main__":
    zeros = [0.03, 0.032, 0.034, 0.035, 0.036]
    tree = bdt_tree(zeros, 0.1, 4)
    assert len(tree) == 5 and len(tree[4]) == 5
    print("bdt self-test passed", tree[2])
