"""Adaptive hierarchical timestep engine for N-body systems."""
from __future__ import annotations
import math
from typing import Callable, List, Tuple

Vec = List[float]


def individual_timesteps(
    pos: List[Vec],
    vel: List[Vec],
    acc: List[Vec],
    eta: float = 0.02,
    dt_min: float = 1e-6,
    dt_max: float = 0.1,
) -> List[float]:
    dts = []
    for i in range(len(pos)):
        a_mag = math.sqrt(sum(x * x for x in acc[i])) + 1e-30
        v_mag = math.sqrt(sum(x * x for x in vel[i])) + 1e-30
        dt_acc = eta / math.sqrt(a_mag)
        dt_cfl = eta * v_mag / a_mag if a_mag > 0 else dt_max
        dt = max(dt_min, min(dt_max, min(dt_acc, dt_cfl)))
        dts.append(dt)
    return dts


def block_timesteps(dts: List[float], dt_max: float) -> List[float]:
    blocks = []
    for dt in dts:
        level = 0
        t = dt_max
        while t > dt and level < 20:
            t *= 0.5
            level += 1
        blocks.append(t)
    return blocks


def collision_aware_dt(
    pos: List[Vec],
    vel: List[Vec],
    radii: List[float],
    safety: float = 0.5,
) -> float:
    dt = float("inf")
    n = len(pos)
    for i in range(n):
        for j in range(i + 1, n):
            rvec = [pos[j][d] - pos[i][d] for d in range(len(pos[0]))]
            vvec = [vel[j][d] - vel[i][d] for d in range(len(vel[0]))]
            r = math.sqrt(sum(x * x for x in rvec))
            v_close = -sum(rvec[d] * vvec[d] for d in range(len(rvec))) / (r + 1e-30)
            if v_close > 0:
                gap = r - radii[i] - radii[j]
                if gap > 0:
                    dt = min(dt, safety * gap / v_close)
    return dt if dt < float("inf") else 1.0


if __name__ == "__main__":
    pos = [[0.0, 0.0], [1.0, 0.0]]
    vel = [[0.0, 0.0], [-0.1, 0.0]]
    acc = [[0.1, 0.0], [-0.1, 0.0]]
    dts = individual_timesteps(pos, vel, acc)
    assert all(d > 0 for d in dts)
    blocks = block_timesteps(dts, 0.1)
    assert all(b > 0 for b in blocks)
    dt_col = collision_aware_dt(pos, vel, [0.01, 0.01])
    assert dt_col > 0
    print(f"adaptive_timestep dts={dts} col={dt_col:.4f}")
    print("adaptive_timestep self-tests passed")
