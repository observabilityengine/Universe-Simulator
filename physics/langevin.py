"""Overdamped Langevin dynamics (Brownian motion in a potential).

Complexity: O(steps).
dx = -grad_V(x) dt + sqrt(2 gamma kT / gamma) dW  (overdamped form).
Original implementation using Euler–Maruyama.
"""
from __future__ import annotations

import numpy as np
from typing import Callable, Tuple


def langevin_overdamped(
    x0: np.ndarray,
    grad_V: Callable[[np.ndarray], np.ndarray],
    dt: float,
    steps: int,
    kT: float = 1.0,
    gamma: float = 1.0,
    seed: int | None = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Integrate overdamped Langevin; returns (final_x, trajectory)."""
    rng = np.random.default_rng(seed)
    x = np.array(x0, dtype=float, copy=True)
    traj = np.empty((steps + 1,) + x.shape)
    traj[0] = x
    noise_scale = np.sqrt(2.0 * kT * dt / gamma)
    for t in range(steps):
        force = -grad_V(x)
        x = x + (force / gamma) * dt + noise_scale * rng.normal(size=x.shape)
        traj[t + 1] = x
    return x, traj


if __name__ == "__main__":
    # Harmonic potential V = 0.5 k x^2, grad = k x
    def grad(x):
        return x.copy()

    x_final, traj = langevin_overdamped(
        np.array([2.0]), grad, dt=0.01, steps=500, kT=0.0, seed=0
    )
    # With kT=0 should relax toward 0
    assert abs(x_final[0]) < 0.5
    assert traj.shape[0] == 501
    x0 = np.array([0.0, 0.0])
    xf, _ = langevin_overdamped(x0, grad, 0.01, 0, seed=1)
    assert np.allclose(xf, x0)
    print("langevin self-tests passed")
