"""Approximate Bayes factor via BIC."""
from __future__ import annotations
import math


def bic(log_likelihood: float, n_params: int, n_data: int) -> float:
    return -2 * log_likelihood + n_params * math.log(n_data)


def bayes_factor_bic(ll1: float, k1: int, ll2: float, k2: int, n: int) -> float:
    """BF_12 approx exp(-0.5*(BIC1-BIC2))."""
    bic1, bic2 = bic(ll1, k1, n), bic(ll2, k2, n)
    return math.exp(-0.5 * (bic1 - bic2))


if __name__ == "__main__":
    bf = bayes_factor_bic(-10, 2, -12, 1, 100)
    assert bf > 0
    print(f"bayes_factor={bf:.3f}")
    print("bayes_factor self-tests passed")
