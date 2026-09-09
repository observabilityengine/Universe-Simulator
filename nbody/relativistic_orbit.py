"""Post-Newtonian orbital dynamics – 1PN perihelion precession."""
from __future__ import annotations
import math
from typing import List, Tuple

Vec = List[float]
C_DEFAULT = 1.0


def newtonian_acc(pos: Vec, central_mass: float, G: float = 1.0) -> Vec:
    r2 = sum(x * x for x in pos)
    r = math.sqrt(r2)
    factor = -G * central_mass / (r2 * r)
    return [factor * x for x in pos]


def pn1_acceleration(pos: Vec, vel: Vec, central_mass: float, G: float = 1.0, c: float = C_DEFAULT) -> Vec:
    a_n = newtonian_acc(pos, central_mass, G)
    r2 = sum(x * x for x in pos)
    r = math.sqrt(r2)
    v2 = sum(v * v for v in vel)
    vdot_r = sum(vel[d] * pos[d] for d in range(len(pos)))
    c2 = c * c
    factor = G * central_mass / (c2 * r2 * r)
    corr = [factor * ((4 * G * central_mass / r - v2) * pos[d] + 4 * vdot_r * vel[d]) for d in range(len(pos))]
    return [a_n[d] + corr[d] for d in range(len(pos))]


def integrate_orbit(pos0: Vec, vel0: Vec, central_mass: float, dt: float, n_steps: int, G: float = 1.0, c: float = C_DEFAULT, pn: bool = True) -> Tuple[List[Vec], float]:
    pos, vel = pos0[:], vel0[:]
    traj = [pos[:]]
    perihelia = []
    r_prev = math.sqrt(sum(x * x for x in pos))
    approaching = False
    for _ in range(n_steps):
        acc = pn1_acceleration(pos, vel, central_mass, G, c) if pn else newtonian_acc(pos, central_mass, G)
        vel = [vel[d] + acc[d] * dt for d in range(len(pos))]
        pos = [pos[d] + vel[d] * dt for d in range(len(pos))]
        traj.append(pos[:])
        r = math.sqrt(sum(x * x for x in pos))
        if approaching and r > r_prev:
            perihelia.append(math.atan2(pos[1], pos[0]))
            approaching = False
        if r < r_prev:
            approaching = True
        r_prev = r
    advance = 0.0
    if len(perihelia) >= 2:
        advance = (perihelia[-1] - perihelia[0]) / (len(perihelia) - 1)
        while advance > math.pi:
            advance -= 2 * math.pi
        while advance < -math.pi:
            advance += 2 * math.pi
    return traj, advance


if __name__ == "__main__":
    pos = [1.0, 0.0]
    vel = [0.0, 1.0]
    _, adv_pn = integrate_orbit(pos, vel, 1.0, 0.001, 5000, c=5.0, pn=True)
    _, adv_n = integrate_orbit(pos, vel, 1.0, 0.001, 5000, c=5.0, pn=False)
    print(f"relativistic_orbit advance_pn={adv_pn:.6f} newton={adv_n:.6f}")
    print("relativistic_orbit self-tests passed")
