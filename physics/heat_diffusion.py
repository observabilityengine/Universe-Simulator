"""1-D heat equation finite-difference solver (explicit FTCS).

Complexity: O(steps * n).
Stability requires r = alpha * dt / dx^2 <= 0.5.
Dirichlet boundaries.
"""
from __future__ import annotations

import numpy as np


def heat_diffusion(
    u0: np.ndarray,
    alpha: float,
    dx: float,
    dt: float,
    steps: int,
    left: float = 0.0,
    right: float = 0.0,
) -> np.ndarray:
    """Evolve initial temperature u0 for given steps. Returns final u."""
    u = np.array(u0, dtype=float, copy=True)
    n = len(u)
    if n < 2:
        return u
    r = alpha * dt / (dx * dx)
    if r > 0.5 + 1e-12:
        raise ValueError("unstable: r > 0.5")
    for _ in range(steps):
        u_new = u.copy()
        u_new[0] = left
        u_new[-1] = right
        for i in range(1, n - 1):
            u_new[i] = u[i] + r * (u[i + 1] - 2 * u[i] + u[i - 1])
        u = u_new
    return u


if __name__ == "__main__":
    u0 = np.array([0., 1., 2., 3., 4.])
    u = heat_diffusion(u0, 1.0, 1.0, 0.1, 100, left=0.0, right=4.0)
    assert np.allclose(u, np.linspace(0, 4, 5), atol=1e-6)
    assert np.allclose(heat_diffusion(u0, 1.0, 1.0, 0.1, 0), u0)
    try:
        heat_diffusion(np.zeros(5), 1.0, 1.0, 1.0, 1)
        assert False
    except ValueError:
        pass
    assert heat_diffusion(np.array([5.]), 1.0, 1.0, 0.1, 10)[0] == 5.0
    print("heat_diffusion self-tests passed")
