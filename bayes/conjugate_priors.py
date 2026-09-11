"""Conjugate prior update helpers."""
from __future__ import annotations
from typing import Tuple


def beta_binomial_update(alpha: float, beta: float, successes: int, trials: int) -> Tuple[float, float]:
    return alpha + successes, beta + (trials - successes)


def normal_normal_update(mu0: float, tau0: float, data_mean: float, data_n: int, data_var: float) -> Tuple[float, float]:
    tau_n = tau0 + data_n / data_var
    mu_n = (tau0 * mu0 + data_n * data_mean / data_var) / tau_n
    return mu_n, tau_n


def gamma_poisson_update(a: float, b: float, total_counts: float, n_obs: float) -> Tuple[float, float]:
    return a + total_counts, b + n_obs


if __name__ == "__main__":
    a, b = beta_binomial_update(1, 1, 7, 10)
    assert a == 8 and b == 4
    print(f"conjugate_priors beta={a},{b}")
    print("conjugate_priors self-tests passed")
