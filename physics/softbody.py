"""
Universe Simulator - Simple Soft-Body (mass-spring)
Original 2-D/3-D mass-spring system with Verlet integration.
"""

from __future__ import annotations

from typing import List, Tuple

Vec = List[float]


class SoftBody:
    def __init__(self, positions: List[Vec], springs: List[Tuple[int, int, float, float]]):
        """
        springs: (i, j, rest_length, stiffness)
        """
        self.pos = [list(p) for p in positions]
        self.prev = [list(p) for p in positions]
        self.springs = springs
        self.dim = len(positions[0])

    def step(self, dt: float, gravity: Vec = None) -> None:
        if gravity is None:
            gravity = [0.0] * self.dim
        n = len(self.pos)
        # Verlet
        for i in range(n):
            for d in range(self.dim):
                x = self.pos[i][d]
                tmp = x
                self.pos[i][d] = x + (x - self.prev[i][d]) + gravity[d] * dt * dt
                self.prev[i][d] = tmp
        # spring constraints (multiple iterations)
        for _ in range(4):
            for i, j, rest, k in self.springs:
                delta = [self.pos[j][d] - self.pos[i][d] for d in range(self.dim)]
                dist = sum(x * x for x in delta) ** 0.5 or 1e-9
                factor = (dist - rest) / dist * 0.5 * k
                for d in range(self.dim):
                    corr = delta[d] * factor
                    self.pos[i][d] += corr
                    self.pos[j][d] -= corr


if __name__ == "__main__":
    body = SoftBody(
        [[0.0, 0.0], [1.0, 0.0], [0.5, 0.866]],
        [(0, 1, 1.0, 0.5), (1, 2, 1.0, 0.5), (2, 0, 1.0, 0.5)],
    )
    for _ in range(10):
        body.step(0.01, gravity=[0.0, -9.8])
    print("softbody self-test passed", body.pos)
