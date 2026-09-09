"""N-Body gravitational integrator with symplectic steps, adaptive dt, conservation checks."""
from __future__ import annotations
import math
from typing import List
from .symplectic_integrator import verlet_step, kinetic_energy

Vec = List[float]
G_DEFAULT = 1.0


def pairwise_acceleration(pos: List[Vec], masses: List[float], G: float = G_DEFAULT, softening: float = 1e-4) -> List[Vec]:
    n = len(pos)
    dim = len(pos[0])
    acc = [[0.0] * dim for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            rvec = [pos[j][d] - pos[i][d] for d in range(dim)]
            r2 = sum(x * x for x in rvec) + softening * softening
            r = math.sqrt(r2)
            inv_r3 = 1.0 / (r2 * r)
            for d in range(dim):
                f = G * rvec[d] * inv_r3
                acc[i][d] += masses[j] * f
                acc[j][d] -= masses[i] * f
    return acc


def potential_energy(pos: List[Vec], masses: List[float], G: float = G_DEFAULT, softening: float = 1e-4) -> float:
    n = len(pos)
    pe = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            r2 = sum((pos[j][d] - pos[i][d]) ** 2 for d in range(len(pos[0]))) + softening ** 2
            pe -= G * masses[i] * masses[j] / math.sqrt(r2)
    return pe


def total_momentum(masses: List[float], vel: List[Vec]) -> List[float]:
    dim = len(vel[0])
    p = [0.0] * dim
    for i in range(len(masses)):
        for d in range(dim):
            p[d] += masses[i] * vel[i][d]
    return p


class NBodySystem:
    def __init__(self, pos: List[Vec], vel: List[Vec], masses: List[float], G: float = G_DEFAULT, softening: float = 1e-4):
        self.pos = [p[:] for p in pos]
        self.vel = [v[:] for v in vel]
        self.masses = masses[:]
        self.G = G
        self.softening = softening
        self.time = 0.0

    def accelerations(self) -> List[Vec]:
        return pairwise_acceleration(self.pos, self.masses, self.G, self.softening)

    def step(self, dt: float) -> None:
        acc_fn = lambda p: pairwise_acceleration(p, self.masses, self.G, self.softening)
        self.pos, self.vel = verlet_step(self.pos, self.vel, acc_fn, dt)
        self.time += dt

    def energy(self) -> float:
        return kinetic_energy(self.masses, self.vel) + potential_energy(self.pos, self.masses, self.G, self.softening)

    def adaptive_step(self, dt_max: float = 0.01, eta: float = 0.01) -> float:
        acc = self.accelerations()
        max_a = max(math.sqrt(sum(a ** 2 for a in acc[i])) for i in range(len(acc))) or 1e-30
        dt = min(dt_max, eta / math.sqrt(max_a))
        self.step(dt)
        return dt


if __name__ == "__main__":
    pos = [[1.0, 0.0], [-1.0, 0.0]]
    vel = [[0.0, 0.5], [0.0, -0.5]]
    masses = [1.0, 1.0]
    sys = NBodySystem(pos, vel, masses, G=1.0)
    e0 = sys.energy()
    for _ in range(200):
        sys.step(0.01)
    e1 = sys.energy()
    assert abs(e1 - e0) / abs(e0) < 0.05
    p = total_momentum(sys.masses, sys.vel)
    assert abs(p[0]) < 1e-6 and abs(p[1]) < 1e-6
    print(f"nbody_integrator dE/E={abs(e1-e0)/abs(e0):.2e}")
    print("nbody_integrator self-tests passed")
