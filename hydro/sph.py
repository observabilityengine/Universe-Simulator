"""Smoothed Particle Hydrodynamics – density, pressure forces, artificial viscosity."""
from __future__ import annotations
import math
from typing import List

Vec = List[float]


def cubic_spline_kernel(r: float, h: float, dim: int = 2) -> float:
    q = r / h
    sigma = 10 / (7 * math.pi * h * h) if dim == 2 else 1 / (math.pi * h ** 3)
    if q < 1:
        return sigma * (1 - 1.5 * q * q + 0.75 * q ** 3)
    if q < 2:
        return sigma * 0.25 * (2 - q) ** 3
    return 0.0


def kernel_grad(rvec: Vec, h: float, dim: int = 2) -> Vec:
    r = math.sqrt(sum(x * x for x in rvec)) + 1e-30
    q = r / h
    sigma = 10 / (7 * math.pi * h * h) if dim == 2 else 1 / (math.pi * h ** 3)
    if q < 1:
        dWdq = sigma * (-3 * q + 2.25 * q * q)
    elif q < 2:
        dWdq = sigma * (-0.75 * (2 - q) ** 2)
    else:
        return [0.0] * len(rvec)
    return [dWdq / h * rvec[d] / r for d in range(len(rvec))]


def estimate_density(pos: List[Vec], masses: List[float], h: float) -> List[float]:
    n = len(pos)
    rho = [0.0] * n
    for i in range(n):
        for j in range(n):
            rvec = [pos[i][d] - pos[j][d] for d in range(len(pos[0]))]
            r = math.sqrt(sum(x * x for x in rvec))
            rho[i] += masses[j] * cubic_spline_kernel(r, h, len(pos[0]))
    return rho


def pressure_eos(rho: float, K: float = 1.0, gamma: float = 5.0 / 3.0) -> float:
    return K * rho ** gamma


def sph_acceleration(pos: List[Vec], vel: List[Vec], masses: List[float], h: float, K: float = 1.0, gamma: float = 5.0 / 3.0, alpha_visc: float = 1.0) -> List[Vec]:
    rho = estimate_density(pos, masses, h)
    P = [pressure_eos(r, K, gamma) for r in rho]
    n = len(pos)
    dim = len(pos[0])
    acc = [[0.0] * dim for _ in range(n)]
    cs = [math.sqrt(gamma * P[i] / max(rho[i], 1e-30)) for i in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            rvec = [pos[i][d] - pos[j][d] for d in range(dim)]
            r = math.sqrt(sum(x * x for x in rvec)) + 1e-30
            grad = kernel_grad(rvec, h, dim)
            term = P[i] / (rho[i] ** 2) + P[j] / (rho[j] ** 2)
            vrel = [vel[i][d] - vel[j][d] for d in range(dim)]
            vdot_r = sum(vrel[d] * rvec[d] for d in range(dim))
            if vdot_r < 0:
                mu = h * vdot_r / (r * r + 0.01 * h * h)
                pi_ij = (-alpha_visc * (cs[i] + cs[j]) / 2 * mu) / ((rho[i] + rho[j]) / 2)
                term += pi_ij
            for d in range(dim):
                acc[i][d] -= masses[j] * term * grad[d]
    return acc


if __name__ == "__main__":
    pos = [[0.0, 0.0], [0.1, 0.0], [0.0, 0.1]]
    vel = [[0.0, 0.0]] * 3
    masses = [1.0, 1.0, 1.0]
    rho = estimate_density(pos, masses, h=0.2)
    assert all(r > 0 for r in rho)
    acc = sph_acceleration(pos, vel, masses, h=0.2)
    print(f"sph density={rho}")
    print("sph self-tests passed")
