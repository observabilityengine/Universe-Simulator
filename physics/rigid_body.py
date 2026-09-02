"""
Universe Simulator - 2-D Rigid Body (position + orientation)
Original velocity-Verlet style integration with torque.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class RigidBody2D:
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    omega: float = 0.0
    mass: float = 1.0
    inertia: float = 1.0

    def apply_force(self, fx: float, fy: float, dt: float) -> None:
        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax * dt
        self.vy += ay * dt

    def apply_torque(self, tau: float, dt: float) -> None:
        self.omega += (tau / self.inertia) * dt

    def integrate(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.theta += self.omega * dt
        # wrap angle
        self.theta = (self.theta + math.pi) % (2 * math.pi) - math.pi


if __name__ == "__main__":
    body = RigidBody2D(mass=2.0, inertia=0.5)
    body.apply_force(4.0, 0.0, 0.1)
    body.apply_torque(1.0, 0.1)
    body.integrate(0.1)
    assert abs(body.vx - 0.2) < 1e-9
    assert abs(body.omega - 0.2) < 1e-9
    print("rigid_body self-test passed", body.x, body.theta)
