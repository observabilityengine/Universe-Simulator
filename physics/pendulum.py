"""Simple pendulum integration (RK4).

Complexity: O(steps). Original implementation.
"""
from __future__ import annotations

from typing import List, Tuple
import math


def pendulum_rk4(
    theta0: float = 0.5,
    omega0: float = 0.0,
    g: float = 9.81,
    L: float = 1.0,
    dt: float = 0.01,
    steps: int = 1000,
) -> Tuple[List[float], List[float]]:
    theta, omega = theta0, omega0
    thetas = [theta]
    omegas = [omega]

    def deriv(th, om):
        return om, -(g / L) * math.sin(th)

    for _ in range(steps):
        k1_th, k1_om = deriv(theta, omega)
        k2_th, k2_om = deriv(theta + 0.5 * dt * k1_th, omega + 0.5 * dt * k1_om)
        k3_th, k3_om = deriv(theta + 0.5 * dt * k2_th, omega + 0.5 * dt * k2_om)
        k4_th, k4_om = deriv(theta + dt * k3_th, omega + dt * k3_om)
        theta += dt * (k1_th + 2 * k2_th + 2 * k3_th + k4_th) / 6
        omega += dt * (k1_om + 2 * k2_om + 2 * k3_om + k4_om) / 6
        thetas.append(theta)
        omegas.append(omega)
    return thetas, omegas


if __name__ == "__main__":
    th, om = pendulum_rk4(theta0=0.1, steps=500)
    assert max(th) > 0.05
    assert min(th) < -0.05
    print("pendulum self-tests passed")
