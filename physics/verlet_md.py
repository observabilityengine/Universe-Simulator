"""Velocity-Verlet molecular dynamics for LJ particles in a box.

Complexity: O(steps * n^2). Original implementation.
"""
from __future__ import annotations
import math
from typing import List, Tuple

def verlet_md(
    n_particles: int = 8, box: float = 10.0, temperature: float = 1.0,
    steps: int = 200, dt: float = 0.005, seed: int = 42,
) -> Tuple[List[List[float]], float]:
    import random
    rng = random.Random(seed)
    pos = []
    n_side = int(math.ceil(n_particles ** 0.5))
    spacing = box / (n_side + 1)
    k = 0
    for i in range(n_side):
        for j in range(n_side):
            if k >= n_particles:
                break
            pos.append([spacing * (i + 1), spacing * (j + 1)])
            k += 1
    pos = pos[:n_particles]
    vel = [[rng.gauss(0, math.sqrt(temperature)) for _ in range(2)] for _ in range(n_particles)]
    vx = sum(v[0] for v in vel) / n_particles
    vy = sum(v[1] for v in vel) / n_particles
    for v in vel:
        v[0] -= vx
        v[1] -= vy

    def forces(positions):
        F = [[0.0, 0.0] for _ in range(n_particles)]
        pot = 0.0
        cutoff2 = 6.25
        for i in range(n_particles):
            for j in range(i + 1, n_particles):
                dx = positions[i][0] - positions[j][0]
                dy = positions[i][1] - positions[j][1]
                dx -= box * round(dx / box)
                dy -= box * round(dy / box)
                r2 = dx * dx + dy * dy
                if r2 < cutoff2 and r2 > 1e-8:
                    r2i = 1.0 / r2
                    r6i = r2i * r2i * r2i
                    lj = 24.0 * r6i * (2.0 * r6i - 1.0) * r2i
                    F[i][0] += lj * dx
                    F[i][1] += lj * dy
                    F[j][0] -= lj * dx
                    F[j][1] -= lj * dy
                    pot += 4.0 * r6i * (r6i - 1.0)
        return F, pot

    F, pot = forces(pos)
    for _ in range(steps):
        for i in range(n_particles):
            vel[i][0] += 0.5 * dt * F[i][0]
            vel[i][1] += 0.5 * dt * F[i][1]
            pos[i][0] = (pos[i][0] + dt * vel[i][0]) % box
            pos[i][1] = (pos[i][1] + dt * vel[i][1]) % box
        F, pot = forces(pos)
        for i in range(n_particles):
            vel[i][0] += 0.5 * dt * F[i][0]
            vel[i][1] += 0.5 * dt * F[i][1]
    kin = 0.5 * sum(v[0] ** 2 + v[1] ** 2 for v in vel)
    return pos, pot + kin

if __name__ == "__main__":
    pos, energy = verlet_md(n_particles=6, steps=100, seed=1)
    assert len(pos) == 6
    assert all(len(p) == 2 for p in pos)
    assert math.isfinite(energy)
    print("verlet_md self-tests passed")
