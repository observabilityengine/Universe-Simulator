"""Normal-Normal conjugate model with known variance."""
from __future__ import annotations
from typing import Tuple


def posterior(mu0: float, prec0: float, data_mean: float, n: int, data_var: float) -> Tuple[float, float]:
    prec_n = prec0 + n / data_var
    mu_n = (prec0 * mu0 + n * data_mean / data_var) / prec_n
    return mu_n, prec_n


if __name__ == "__main__":
    mu, prec = posterior(0, 1, 5, 10, 1)
    assert mu > 0
    print(f"normal_normal mu={mu:.3f}")
    print("normal_normal self-tests passed")
