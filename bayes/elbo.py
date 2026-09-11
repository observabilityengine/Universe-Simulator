"""Evidence Lower Bound for Gaussian mean-field."""
from __future__ import annotations
import math


def gaussian_elbo(m: float, s: float, data: list, prior_prec: float = 1.0) -> float:
    n = len(data)
    data_mean = sum(data) / n
    # E[log p(data|mu)] - KL(q||prior)
    expected_ll = -0.5 * n * (s ** 2 + (m - data_mean) ** 2 + sum((x - data_mean) ** 2 for x in data) / n)
    kl = 0.5 * (prior_prec * (s ** 2 + m ** 2) - 1 - math.log(prior_prec * s ** 2 + 1e-12))
    return expected_ll - kl


if __name__ == "__main__":
    e = gaussian_elbo(0.0, 1.0, [0.0, 0.1, -0.1])
    assert e < 0
    print(f"elbo={e:.3f}")
    print("elbo self-tests passed")
