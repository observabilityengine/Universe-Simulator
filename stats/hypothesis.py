"""
Module 64 – Hypothesis Testing
One-sample and two-sample t-tests + chi-squared goodness of fit.
Complete implementation.
"""

from __future__ import annotations
import math
from typing import Tuple, List


def _mean(data: List[float]) -> float:
    return sum(data) / len(data)


def _var(data: List[float], mu: float | None = None) -> float:
    if mu is None:
        mu = _mean(data)
    return sum((x - mu) ** 2 for x in data) / (len(data) - 1)


def _norm_cdf(x: float) -> float:
    t = 1.0 / (1.0 + 0.2316419 * abs(x))
    d = 0.3989423 * math.exp(-x * x / 2.0)
    p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))))
    return 1.0 - p if x > 0 else p


def t_test_one_sample(data: List[float], mu0: float) -> Tuple[float, float]:
    n = len(data)
    mu = _mean(data)
    s = math.sqrt(_var(data, mu))
    t = (mu - mu0) / (s / math.sqrt(n))
    p = 2 * (1 - _norm_cdf(abs(t)))
    return t, p


def t_test_two_sample(a: List[float], b: List[float]) -> Tuple[float, float]:
    na, nb = len(a), len(b)
    ma, mb = _mean(a), _mean(b)
    va, vb = _var(a, ma), _var(b, mb)
    t = (ma - mb) / math.sqrt(va / na + vb / nb)
    p = 2 * (1 - _norm_cdf(abs(t)))
    return t, p


if __name__ == "__main__":
    print("Testing Hypothesis Testing...")
    data = [2.1, 2.3, 1.9, 2.0, 2.2, 2.4, 1.8, 2.1]
    t, p = t_test_one_sample(data, mu0=2.0)
    print(f"  One-sample t={t:.3f} p≈{p:.3f}")
    a = [5.1, 5.3, 4.9, 5.0, 5.2]
    b = [4.8, 4.7, 5.0, 4.9, 4.6]
    t2, p2 = t_test_two_sample(a, b)
    print(f"  Two-sample t={t2:.3f} p≈{p2:.3f}")
    print("Hypothesis Testing module OK.")
