"""
Universe Simulator - Nelson-Siegel yield curve
Original parametric form + simple fit by grid.
"""

from __future__ import annotations

import math
from typing import List, Tuple

def ns_rate(t: float, beta0: float, beta1: float, beta2: float, tau: float) -> float:
    if t < 1e-8:
        return beta0 + beta1
    x = t / tau
    return beta0 + beta1 * (1 - math.exp(-x)) / x + beta2 * ((1 - math.exp(-x)) / x - math.exp(-x))

def fit_ns(tenors: List[float], rates: List[float]) -> Tuple[float, float, float, float]:
    best = (0.03, -0.02, 0.01, 1.5)
    best_err = float("inf")
    for b0 in [0.01, 0.02, 0.03, 0.04]:
        for b1 in [-0.03, -0.02, -0.01, 0.0]:
            for b2 in [-0.02, 0.0, 0.02, 0.04]:
                for tau in [0.5, 1.0, 1.5, 2.0]:
                    err = sum((ns_rate(t, b0, b1, b2, tau) - r) ** 2 for t, r in zip(tenors, rates))
                    if err < best_err:
                        best_err = err
                        best = (b0, b1, b2, tau)
    return best

if __name__ == "__main__":
    tenors = [0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
    rates = [0.02, 0.022, 0.025, 0.03, 0.035, 0.04]
    b0, b1, b2, tau = fit_ns(tenors, rates)
    assert abs(ns_rate(1.0, b0, b1, b2, tau) - 0.025) < 0.01
    print("nelson_siegel self-test passed", b0, b1, b2, tau)
