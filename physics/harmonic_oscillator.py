"""Analytic and numeric simple harmonic oscillator.

Complexity: O(1) analytic; O(steps) numeric Euler–Cromer.
x'' = -ω² x. Original implementation.
"""
from __future__ import annotations

import math
from typing import Tuple
import numpy as np


def sho_analytic(
    t: float,
    x0: float,
    v0: float,
    omega: float,
) -> Tuple[float, float]:
    """Exact position and velocity at time t."""
    x = x0 * math.cos(omega * t) + (v0 / omega) * math.sin(omega * t) if omega != 0 else x0 + v0 * t
    v = -x0 * omega * math.sin(omega * t) + v0 * math.cos(omega * t) if omega != 0 else v0
    return x, v


def sho_euler_cromer(
    x0: float,
    v0: float,
    omega: float,
    dt: float,
    steps: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """Numeric trajectory via Euler–Cromer (semi-implicit Euler)."""
    x = np.empty(steps + 1)
    v = np.empty(steps + 1)
    x[0], v[0] = x0, v0
    for i in range(steps):
        v[i + 1] = v[i] - omega * omega * x[i] * dt
        x[i + 1] = x[i] + v[i + 1] * dt
    return x, v


if __name__ == "__main__":
    # period T=2π for omega=1, back to start
    x, v = sho_analytic(2 * math.pi, 1.0, 0.0, 1.0)
    assert abs(x - 1.0) < 1e-12 and abs(v) < 1e-12
    xs, vs = sho_euler_cromer(1.0, 0.0, 1.0, 0.001, 1000)
    # energy roughly conserved
    e0 = 0.5 * 0.0**2 + 0.5 * 1.0**2 * 1.0**2
    e1 = 0.5 * vs[-1] ** 2 + 0.5 * 1.0**2 * xs[-1] ** 2
    assert abs(e1 - e0) < 0.05
    print("harmonic_oscillator self-tests passed")
