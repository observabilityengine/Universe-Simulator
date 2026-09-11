"""Gamma-Poisson conjugate model."""
from __future__ import annotations
from typing import Tuple


def posterior(a: float, b: float, total: float, n: float) -> Tuple[float, float]:
    return a + total, b + n


def mean_rate(a: float, b: float) -> float:
    return a / b


if __name__ == "__main__":
    a, b = posterior(1, 1, 20, 10)
    assert abs(mean_rate(a, b) - 2.0) < 1e-9
    print(f"gamma_poisson rate={mean_rate(a,b)}")
    print("gamma_poisson self-tests passed")
