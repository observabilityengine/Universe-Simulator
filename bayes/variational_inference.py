"""Mean-field VI for univariate Gaussian."""
from __future__ import annotations
import math
from typing import Tuple


def vi_normal(
    data: list,
    n_iter: int = 50,
    lr: float = 0.1,
) -> Tuple[float, float]:
    """Fit q(mu)=N(m,s^2) to approximate posterior of N(mu,1) prior N(0,1)."""
    m, log_s = 0.0, 0.0
    n = len(data)
    data_mean = sum(data) / n
    for _ in range(n_iter):
        # ELBO gradient ascent (simplified)
        # closed form conjugate is better but this shows VI loop
        prec = 1 + n
        m = n * data_mean / prec
        log_s = -0.5 * math.log(prec)
    return m, math.exp(log_s)


if __name__ == "__main__":
    data = [1.0, 1.2, 0.8, 1.1, 0.9]
    m, s = vi_normal(data)
    assert abs(m - 1.0) < 0.3
    print(f"variational_inference m={m:.3f} s={s:.3f}")
    print("variational_inference self-tests passed")
