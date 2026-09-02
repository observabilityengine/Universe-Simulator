"""
Universe Simulator - EM for 1-D two-component Gaussian Mixture
Original Expectation-Maximization.
"""

from __future__ import annotations

import math
from typing import List, Tuple


def _gauss(x: float, mu: float, var: float) -> float:
    return math.exp(-0.5 * (x - mu) ** 2 / var) / math.sqrt(2 * math.pi * var)


def em_gmm_1d(
    data: List[float],
    max_iter: int = 50,
) -> Tuple[float, float, float, float, float]:
    """Returns mu1, mu2, var1, var2, pi."""
    n = len(data)
    mu1, mu2 = min(data), max(data)
    var1 = var2 = 1.0
    pi = 0.5
    for _ in range(max_iter):
        # E-step
        resp = []
        for x in data:
            p1 = pi * _gauss(x, mu1, var1)
            p2 = (1 - pi) * _gauss(x, mu2, var2)
            s = p1 + p2 + 1e-12
            resp.append(p1 / s)
        # M-step
        n1 = sum(resp)
        n2 = n - n1
        mu1 = sum(r * x for r, x in zip(resp, data)) / (n1 + 1e-12)
        mu2 = sum((1 - r) * x for r, x in zip(resp, data)) / (n2 + 1e-12)
        var1 = sum(r * (x - mu1) ** 2 for r, x in zip(resp, data)) / (n1 + 1e-12)
        var2 = sum((1 - r) * (x - mu2) ** 2 for r, x in zip(resp, data)) / (n2 + 1e-12)
        var1 = max(var1, 1e-6)
        var2 = max(var2, 1e-6)
        pi = n1 / n
    return mu1, mu2, var1, var2, pi


if __name__ == "__main__":
    data = [-2.0, -1.5, -1.8, -2.2, 3.0, 3.5, 2.8, 3.2, 3.1]
    mu1, mu2, _, _, pi = em_gmm_1d(data)
    assert (mu1 < 0 < mu2) or (mu2 < 0 < mu1)
    print("em_gmm self-test passed", mu1, mu2, pi)
