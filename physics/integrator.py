"""
Universe Simulator - Numerical Integrators
Original Verlet and RK4 integrators for Newtonian dynamics.
"""

from __future__ import annotations

from typing import Callable, List, Tuple

State = Tuple[List[float], List[float]]  # positions, velocities


def verlet_step(
    pos: List[float],
    vel: List[float],
    acc: List[float],
    dt: float,
) -> Tuple[List[float], List[float]]:
    """Velocity-Verlet single step."""
    new_pos = [p + v * dt + 0.5 * a * dt * dt for p, v, a in zip(pos, vel, acc)]
    # caller supplies new acceleration after position update
    return new_pos, vel  # velocity update done by caller with new_acc


def verlet_complete(
    pos: List[float],
    vel: List[float],
    acc: List[float],
    new_acc: List[float],
    dt: float,
) -> Tuple[List[float], List[float]]:
    new_pos = [p + v * dt + 0.5 * a * dt * dt for p, v, a in zip(pos, vel, acc)]
    new_vel = [v + 0.5 * (a + na) * dt for v, a, na in zip(vel, acc, new_acc)]
    return new_pos, new_vel


def rk4_step(
    y: List[float],
    dydt_fn: Callable[[List[float]], List[float]],
    dt: float,
) -> List[float]:
    """Classic RK4 for autonomous system dy/dt = f(y)."""
    k1 = dydt_fn(y)
    y2 = [yi + 0.5 * dt * ki for yi, ki in zip(y, k1)]
    k2 = dydt_fn(y2)
    y3 = [yi + 0.5 * dt * ki for yi, ki in zip(y, k2)]
    k3 = dydt_fn(y3)
    y4 = [yi + dt * ki for yi, ki in zip(y, k3)]
    k4 = dydt_fn(y4)
    return [
        yi + (dt / 6.0) * (k1i + 2 * k2i + 2 * k3i + k4i)
        for yi, k1i, k2i, k3i, k4i in zip(y, k1, k2, k3, k4)
    ]


if __name__ == "__main__":
    # simple harmonic oscillator test
    def f(y):
        x, v = y
        return [v, -x]

    state = [1.0, 0.0]
    dt = 0.01
    for _ in range(100):
        state = rk4_step(state, f, dt)
    energy = 0.5 * (state[0] ** 2 + state[1] ** 2)
    assert abs(energy - 0.5) < 1e-4, energy
    print("integrator self-test passed, energy=", energy)
