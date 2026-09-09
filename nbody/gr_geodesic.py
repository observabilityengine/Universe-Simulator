"""Schwarzschild geodesic integrator for test-particle orbits."""
from __future__ import annotations
import math
from typing import List, Tuple


def schwarzschild_christoffel(r: float, theta: float, M: float) -> dict:
    rs = 2 * M
    if abs(r - rs) < 1e-12 or r < 1e-12:
        r = rs + 1e-6
    G = {}
    G[("t", "t", "r")] = M / (r * r) * (1 - rs / r)
    G[("t", "r", "t")] = G[("t", "t", "r")]
    G[("r", "t", "t")] = M / (r * r) * (1 - rs / r)
    G[("r", "r", "r")] = -M / (r * (r - rs)) if r != rs else 0
    G[("r", "theta", "theta")] = -(r - rs)
    G[("r", "phi", "phi")] = -(r - rs) * math.sin(theta) ** 2
    G[("theta", "r", "theta")] = 1 / r
    G[("theta", "theta", "r")] = 1 / r
    G[("theta", "phi", "phi")] = -math.sin(theta) * math.cos(theta)
    G[("phi", "r", "phi")] = 1 / r
    G[("phi", "phi", "r")] = 1 / r
    G[("phi", "theta", "phi")] = 1 / math.tan(theta) if abs(math.sin(theta)) > 1e-12 else 0
    G[("phi", "phi", "theta")] = G[("phi", "theta", "phi")]
    return G


def geodesic_rhs(y: List[float], M: float) -> List[float]:
    t, r, theta, phi, ut, ur, uth, uph = y
    Gamma = schwarzschild_christoffel(r, theta, M)
    coords = ["t", "r", "theta", "phi"]
    u = [ut, ur, uth, uph]
    du = [0.0] * 4
    for mu_i, mu in enumerate(coords):
        for a_i, a in enumerate(coords):
            for b_i, b in enumerate(coords):
                key = (mu, a, b)
                g = Gamma.get(key, Gamma.get((mu, b, a), 0.0))
                du[mu_i] -= g * u[a_i] * u[b_i]
    return [ut, ur, uth, uph, du[0], du[1], du[2], du[3]]


def rk4_step(y: List[float], M: float, dtau: float) -> List[float]:
    def add(a, b, s):
        return [a[i] + s * b[i] for i in range(len(a))]
    k1 = geodesic_rhs(y, M)
    k2 = geodesic_rhs(add(y, k1, dtau / 2), M)
    k3 = geodesic_rhs(add(y, k2, dtau / 2), M)
    k4 = geodesic_rhs(add(y, k3, dtau), M)
    return [y[i] + dtau / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(y))]


def integrate_geodesic(r0: float, e: float, l: float, M: float = 1.0, n_steps: int = 500, dtau: float = 0.1) -> List[Tuple[float, float]]:
    rs = 2 * M
    f = 1 - rs / r0
    ut = e / f
    uph = l / (r0 * r0)
    term = -1 + f * ut * ut - r0 * r0 * uph * uph
    ur2 = f * term
    ur = math.sqrt(max(0, ur2))
    y = [0.0, r0, math.pi / 2, 0.0, ut, ur, 0.0, uph]
    traj = []
    for _ in range(n_steps):
        traj.append((y[1], y[3]))
        y = rk4_step(y, M, dtau)
        if y[1] < 1.5 * rs:
            break
    return traj


if __name__ == "__main__":
    traj = integrate_geodesic(r0=10.0, e=0.98, l=4.0, M=1.0, n_steps=200)
    assert len(traj) > 10
    rs = [t[0] for t in traj]
    assert min(rs) > 2.0
    print(f"gr_geodesic n_pts={len(traj)} r_range=[{min(rs):.2f},{max(rs):.2f}]")
    print("gr_geodesic self-tests passed")
