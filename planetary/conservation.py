"""Conservation-law validator for N-body / collision systems."""
from __future__ import annotations
import math
from typing import List

Vec = List[float]


def total_mass(masses: List[float]) -> float:
    return sum(masses)


def total_momentum(masses: List[float], velocities: List[Vec]) -> Vec:
    dim = len(velocities[0])
    p = [0.0] * dim
    for m, v in zip(masses, velocities):
        for d in range(dim):
            p[d] += m * v[d]
    return p


def total_energy(masses: List[float], positions: List[Vec], velocities: List[Vec], G: float = 1.0) -> float:
    ke = 0.5 * sum(m * sum(v ** 2 for v in vel) for m, vel in zip(masses, velocities))
    pe = 0.0
    n = len(masses)
    for i in range(n):
        for j in range(i + 1, n):
            r = math.sqrt(sum((positions[i][d] - positions[j][d]) ** 2 for d in range(len(positions[0]))))
            pe -= G * masses[i] * masses[j] / max(r, 1e-12)
    return ke + pe


def relative_drift(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), 1e-30)


def validate_conservation(m0: float, p0: Vec, e0: float, masses: List[float], positions: List[Vec], velocities: List[Vec], tol_mass: float = 1e-10, tol_mom: float = 1e-6, tol_energy: float = 0.05) -> dict:
    m1 = total_mass(masses)
    p1 = total_momentum(masses, velocities)
    e1 = total_energy(masses, positions, velocities)
    return {
        "mass_ok": relative_drift(m0, m1) < tol_mass,
        "momentum_ok": all(abs(p1[d] - p0[d]) < tol_mom for d in range(len(p0))),
        "energy_ok": relative_drift(e0, e1) < tol_energy,
        "dE_E": relative_drift(e0, e1),
    }


if __name__ == "__main__":
    masses = [1.0, 1.0]
    pos = [[1, 0], [-1, 0]]
    vel = [[0, 0.5], [0, -0.5]]
    m0 = total_mass(masses)
    p0 = total_momentum(masses, vel)
    e0 = total_energy(masses, pos, vel)
    report = validate_conservation(m0, p0, e0, masses, pos, vel)
    assert report["mass_ok"] and report["momentum_ok"]
    print(f"conservation {report}")
    print("conservation self-tests passed")
