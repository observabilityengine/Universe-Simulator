"""High-order symplectic integrators: Verlet, Forest-Ruth, Yoshida 4th-order."""
from __future__ import annotations
from typing import Callable, List, Tuple

Vec = List[float]


def verlet_step(pos: List[Vec], vel: List[Vec], acc_fn: Callable[[List[Vec]], List[Vec]], dt: float) -> Tuple[List[Vec], List[Vec]]:
    n = len(pos)
    dim = len(pos[0])
    acc = acc_fn(pos)
    new_pos = [[pos[i][d] + vel[i][d] * dt + 0.5 * acc[i][d] * dt * dt for d in range(dim)] for i in range(n)]
    acc2 = acc_fn(new_pos)
    new_vel = [[vel[i][d] + 0.5 * (acc[i][d] + acc2[i][d]) * dt for d in range(dim)] for i in range(n)]
    return new_pos, new_vel


def forest_ruth_step(pos: List[Vec], vel: List[Vec], acc_fn: Callable[[List[Vec]], List[Vec]], dt: float) -> Tuple[List[Vec], List[Vec]]:
    xi = 1.0 / (2 - 2 ** (1.0 / 3))
    lam = -2 ** (1.0 / 3) / (2 - 2 ** (1.0 / 3))
    p, v = [r[:] for r in pos], [u[:] for u in vel]
    for factor in (xi, lam, xi):
        a = acc_fn(p)
        for i in range(len(p)):
            for d in range(len(p[0])):
                v[i][d] += 0.5 * factor * dt * a[i][d]
                p[i][d] += factor * dt * v[i][d]
        a = acc_fn(p)
        for i in range(len(p)):
            for d in range(len(p[0])):
                v[i][d] += 0.5 * factor * dt * a[i][d]
    return p, v


def yoshida4_step(pos: List[Vec], vel: List[Vec], acc_fn: Callable[[List[Vec]], List[Vec]], dt: float) -> Tuple[List[Vec], List[Vec]]:
    x0 = -2 ** (1.0 / 3) / (2 - 2 ** (1.0 / 3))
    x1 = 1.0 / (2 - 2 ** (1.0 / 3))
    p, v = pos, vel
    for w in (x1, x0, x1):
        p, v = verlet_step(p, v, acc_fn, w * dt)
    return p, v


def kinetic_energy(masses: List[float], vel: List[Vec]) -> float:
    return 0.5 * sum(masses[i] * sum(v ** 2 for v in vel[i]) for i in range(len(masses)))


if __name__ == "__main__":
    def acc(pos):
        return [[-p[0]] for p in pos]
    pos = [[1.0]]
    vel = [[0.0]]
    for _ in range(100):
        pos, vel = verlet_step(pos, vel, acc, 0.01)
    e = 0.5 * (pos[0][0] ** 2 + vel[0][0] ** 2)
    assert abs(e - 0.5) < 0.02
    print(f"symplectic_integrator energy={e:.4f}")
    print("symplectic_integrator self-tests passed")
