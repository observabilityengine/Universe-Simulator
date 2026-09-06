"""Velocity Verlet integrator for N-body or general force fields.

Complexity: O(N) per step for N particles (force evaluation external).
Conserves energy better than Euler. 1-D or multi-D via array shape.
"""
from __future__ import annotations

import numpy as np
from typing import Callable, Tuple


def velocity_verlet(
    x: np.ndarray,
    v: np.ndarray,
    force_fn: Callable[[np.ndarray], np.ndarray],
    mass: float | np.ndarray,
    dt: float,
    steps: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """Integrate x'' = force(x)/mass for given steps.

    Returns final (x, v).
    """
    x = np.array(x, dtype=float, copy=True)
    v = np.array(v, dtype=float, copy=True)
    a = force_fn(x) / mass
    for _ in range(steps):
        x = x + v * dt + 0.5 * a * dt * dt
        a_new = force_fn(x) / mass
        v = v + 0.5 * (a + a_new) * dt
        a = a_new
    return x, v


if __name__ == "__main__":
    def force(x):
        return -x

    x0 = np.array([1.0])
    v0 = np.array([0.0])
    x_final, v_final = velocity_verlet(x0, v0, force, 1.0, 2 * np.pi / 1000, 1000)
    assert abs(x_final[0] - 1.0) < 0.01
    assert abs(v_final[0]) < 0.01

    xf, vf = velocity_verlet(x0, v0, force, 1.0, 0.1, 0)
    assert np.allclose(xf, x0) and np.allclose(vf, v0)

    def zero(x):
        return np.zeros_like(x)
    xf, vf = velocity_verlet(np.array([0.0]), np.array([1.0]), zero, 1.0, 0.5, 2)
    assert abs(xf[0] - 1.0) < 1e-12
    assert abs(vf[0] - 1.0) < 1e-12
    print("verlet self-tests passed")
