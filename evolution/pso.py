"""
Universe Simulator - Particle Swarm Optimization
Original PSO for continuous optimisation.
"""

from __future__ import annotations

import random
from typing import Callable, List, Tuple


def pso(
    objective: Callable[[List[float]], float],
    dim: int,
    bounds: Tuple[float, float],
    n_particles: int = 20,
    iterations: int = 50,
    w: float = 0.7,
    c1: float = 1.5,
    c2: float = 1.5,
    seed: int = 42,
) -> Tuple[List[float], float]:
    rng = random.Random(seed)
    lo, hi = bounds
    pos = [[rng.uniform(lo, hi) for _ in range(dim)] for _ in range(n_particles)]
    vel = [[rng.uniform(-1, 1) for _ in range(dim)] for _ in range(n_particles)]
    pbest = [p[:] for p in pos]
    pbest_val = [objective(p) for p in pos]
    gbest = pbest[min(range(n_particles), key=lambda i: pbest_val[i])][:]
    gbest_val = min(pbest_val)

    for _ in range(iterations):
        for i in range(n_particles):
            for d in range(dim):
                r1, r2 = rng.random(), rng.random()
                vel[i][d] = w * vel[i][d] + c1 * r1 * (pbest[i][d] - pos[i][d]) + c2 * r2 * (gbest[d] - pos[i][d])
                pos[i][d] = max(lo, min(hi, pos[i][d] + vel[i][d]))
            val = objective(pos[i])
            if val < pbest_val[i]:
                pbest_val[i] = val
                pbest[i] = pos[i][:]
                if val < gbest_val:
                    gbest_val = val
                    gbest = pos[i][:]
    return gbest, gbest_val


if __name__ == "__main__":
    def sphere(x):
        return sum(v*v for v in x)
    best, val = pso(sphere, dim=3, bounds=(-5, 5), iterations=40)
    assert val < 0.5
    print("pso self-test passed", best, val)
