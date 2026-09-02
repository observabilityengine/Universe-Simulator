"""
Real N-body gravitational physics engine.
Uses Newtonian gravity with adaptive timestep (scipy ODE integrator).
Fully executable. No mocks.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from typing import Tuple, Optional, Callable
import time


class NBodySystem:
    """
    Newtonian N-body gravitational system.
    Units: G = 1 (dimensionless). Positions and velocities in consistent units.
    """

    def __init__(
        self,
        positions: np.ndarray,
        velocities: np.ndarray,
        masses: np.ndarray,
        soft: float = 1e-4,
    ):
        self.pos = np.asarray(positions, dtype=np.float64)
        self.vel = np.asarray(velocities, dtype=np.float64)
        self.mass = np.asarray(masses, dtype=np.float64)
        self.soft = float(soft)
        self.N = self.pos.shape[0]
        self.G = 1.0
        self.time = 0.0
        self.history: list[Tuple[float, np.ndarray, np.ndarray]] = []

        if self.pos.shape != (self.N, 3):
            raise ValueError("positions must be (N, 3)")
        if self.vel.shape != (self.N, 3):
            raise ValueError("velocities must be (N, 3)")
        if self.mass.shape != (self.N,):
            raise ValueError("masses must be (N,)")

    def accelerations(self, pos: np.ndarray) -> np.ndarray:
        acc = np.zeros_like(pos)
        for i in range(self.N):
            for j in range(i + 1, self.N):
                rvec = pos[j] - pos[i]
                dist2 = np.dot(rvec, rvec) + self.soft ** 2
                dist = np.sqrt(dist2)
                force_mag = self.G / (dist2 * dist)
                force = force_mag * rvec
                acc[i] += force * self.mass[j]
                acc[j] -= force * self.mass[i]
        return acc

    def _derivatives(self, t: float, y: np.ndarray) -> np.ndarray:
        pos = y[: 3 * self.N].reshape(self.N, 3)
        vel = y[3 * self.N :].reshape(self.N, 3)
        acc = self.accelerations(pos)
        return np.concatenate([vel.ravel(), acc.ravel()])

    def step(self, dt: float, method: str = "RK45") -> None:
        y0 = np.concatenate([self.pos.ravel(), self.vel.ravel()])
        sol = solve_ivp(
            self._derivatives,
            (0.0, dt),
            y0,
            method=method,
            rtol=1e-8,
            atol=1e-10,
            dense_output=False,
        )
        if not sol.success:
            raise RuntimeError(f"Integration failed: {sol.message}")
        y_final = sol.y[:, -1]
        self.pos = y_final[: 3 * self.N].reshape(self.N, 3)
        self.vel = y_final[3 * self.N :].reshape(self.N, 3)
        self.time += dt
        self.history.append((self.time, self.pos.copy(), self.vel.copy()))

    def energy(self) -> float:
        ke = 0.5 * np.sum(self.mass[:, None] * self.vel ** 2)
        pe = 0.0
        for i in range(self.N):
            for j in range(i + 1, self.N):
                rvec = self.pos[j] - self.pos[i]
                dist = np.sqrt(np.dot(rvec, rvec) + self.soft ** 2)
                pe -= self.G * self.mass[i] * self.mass[j] / dist
        return ke + pe

    def center_of_mass(self) -> Tuple[np.ndarray, np.ndarray]:
        total_mass = np.sum(self.mass)
        com_pos = np.sum(self.mass[:, None] * self.pos, axis=0) / total_mass
        com_vel = np.sum(self.mass[:, None] * self.vel, axis=0) / total_mass
        return com_pos, com_vel

    def run(
        self,
        total_time: float,
        dt: float = 0.01,
        callback: Optional[Callable[["NBodySystem"], None]] = None,
    ) -> None:
        steps = int(np.ceil(total_time / dt))
        for _ in range(steps):
            self.step(dt)
            if callback is not None:
                callback(self)

    def snapshot(self) -> dict:
        return {
            "time": self.time,
            "positions": self.pos.tolist(),
            "velocities": self.vel.tolist(),
            "masses": self.mass.tolist(),
            "energy": self.energy(),
        }


def create_solar_system() -> NBodySystem:
    masses = np.array([
        1.0, 1.66e-7, 2.45e-6, 3.00e-6, 3.23e-7,
        9.55e-4, 2.86e-4, 4.37e-5, 5.15e-5,
    ])
    a = np.array([0.0, 0.387, 0.723, 1.0, 1.524, 5.203, 9.537, 19.191, 30.069])
    v_circ = np.zeros_like(a)
    v_circ[1:] = 1.0 / np.sqrt(a[1:])
    positions = np.zeros((9, 3))
    positions[:, 0] = a
    velocities = np.zeros((9, 3))
    velocities[:, 1] = v_circ
    return NBodySystem(positions, velocities, masses, soft=1e-6)


if __name__ == "__main__":
    print("Running N-body Solar System test...")
    system = create_solar_system()
    E0 = system.energy()
    print(f"Initial energy: {E0:.8e}")
    start = time.time()
    system.run(total_time=0.1, dt=0.002)
    elapsed = time.time() - start
    E1 = system.energy()
    print(f"Final energy:   {E1:.8e}")
    print(f"Relative energy error: {abs(E1 - E0) / abs(E0):.3e}")
    print(f"Wall time: {elapsed:.3f}s")
    print(f"Final Earth position: {system.pos[3]}")
    print("N-body module OK.")
