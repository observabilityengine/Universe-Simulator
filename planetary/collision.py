"""Planetary collision solver – sticky, bounce, and fragmentation outcomes."""
from __future__ import annotations
import math
from typing import List, Tuple

Vec = List[float]


def reduced_mass(m1: float, m2: float) -> float:
    return m1 * m2 / (m1 + m2)


def impact_parameter_and_velocity(pos1: Vec, vel1: Vec, pos2: Vec, vel2: Vec) -> Tuple[float, float]:
    rvec = [pos2[d] - pos1[d] for d in range(len(pos1))]
    vvec = [vel2[d] - vel1[d] for d in range(len(vel1))]
    r = math.sqrt(sum(x * x for x in rvec)) + 1e-30
    v_rel = math.sqrt(sum(x * x for x in vvec))
    if len(rvec) >= 2:
        cross = abs(rvec[0] * vvec[1] - rvec[1] * vvec[0])
        b = cross / (v_rel + 1e-30)
    else:
        b = 0.0
    return b, v_rel


def collision_outcome(m1: float, m2: float, r1: float, r2: float, v_rel: float, b: float, v_esc_factor: float = 1.0) -> str:
    mu = reduced_mass(m1, m2)
    v_esc = math.sqrt(2 * (m1 + m2) / max(r1 + r2, 1e-12)) * v_esc_factor
    E_kin = 0.5 * mu * v_rel ** 2
    E_bind = 0.5 * mu * v_esc ** 2
    b_max = r1 + r2
    if b > b_max:
        return "miss"
    if E_kin < E_bind and b < 0.5 * b_max:
        return "merge"
    if E_kin < 2 * E_bind:
        return "bounce"
    return "fragment"


def merge_bodies(m1: float, m2: float, pos1: Vec, pos2: Vec, vel1: Vec, vel2: Vec) -> Tuple[float, Vec, Vec]:
    m = m1 + m2
    pos = [(m1 * pos1[d] + m2 * pos2[d]) / m for d in range(len(pos1))]
    vel = [(m1 * vel1[d] + m2 * vel2[d]) / m for d in range(len(vel1))]
    return m, pos, vel


if __name__ == "__main__":
    outcome = collision_outcome(1, 1, 0.1, 0.1, 0.1, 0.01)
    assert outcome in ("merge", "bounce", "fragment", "miss")
    m, p, v = merge_bodies(1, 2, [0, 0], [1, 0], [0, 0], [0, 0])
    assert abs(m - 3) < 1e-12
    print(f"collision outcome={outcome}")
    print("collision self-tests passed")
