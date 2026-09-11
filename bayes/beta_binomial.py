"""Beta-Binomial conjugate model."""
from __future__ import annotations
import math
from typing import Tuple


def posterior(alpha: float, beta: float, k: int, n: int) -> Tuple[float, float]:
    return alpha + k, beta + n - k


def posterior_mean(alpha: float, beta: float) -> float:
    return alpha / (alpha + beta)


def posterior_var(alpha: float, beta: float) -> float:
    s = alpha + beta
    return alpha * beta / (s * s * (s + 1))


if __name__ == "__main__":
    a, b = posterior(1, 1, 8, 10)
    assert abs(posterior_mean(a, b) - 0.75) < 1e-9
    print(f"beta_binomial mean={posterior_mean(a,b):.3f}")
    print("beta_binomial self-tests passed")
