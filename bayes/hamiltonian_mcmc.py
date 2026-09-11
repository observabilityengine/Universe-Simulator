"""Hamiltonian Monte Carlo (leapfrog integrator)."""
from __future__ import annotations
import math
import random
from typing import Callable, List


def hmc(
    log_prob: Callable[[float], float],
    grad_log_prob: Callable[[float], float],
    x0: float,
    n_samples: int = 500,
    step_size: float = 0.1,
    n_leapfrog: int = 10,
    seed: int = 42,
) -> List[float]:
    rng = random.Random(seed)
    x = x0
    samples = []
    for _ in range(n_samples):
        p = rng.gauss(0, 1)
        x_new, p_new = x, p
        p_new += 0.5 * step_size * grad_log_prob(x_new)
        for _ in range(n_leapfrog):
            x_new += step_size * p_new
            p_new += step_size * grad_log_prob(x_new)
        p_new -= 0.5 * step_size * grad_log_prob(x_new)
        def H(xx, pp):
            return -log_prob(xx) + 0.5 * pp * pp
        log_alpha = H(x, p) - H(x_new, p_new)
        if math.log(rng.random() + 1e-300) < log_alpha:
            x = x_new
        samples.append(x)
    return samples


if __name__ == "__main__":
    def logp(x):
        return -0.5 * x * x
    def grad(x):
        return -x
    samples = hmc(logp, grad, 0.0, 800, 0.15, 5)
    mean = sum(samples[200:]) / len(samples[200:])
    assert abs(mean) < 0.4
    print(f"hamiltonian_mcmc mean={mean:.3f}")
    print("hamiltonian_mcmc self-tests passed")
