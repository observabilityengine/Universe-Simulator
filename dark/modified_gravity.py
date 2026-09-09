"""Modified gravity – Yukawa/fifth-force and simple f(R)-inspired enhancement."""
from __future__ import annotations
import math
from typing import List

Vec = List[float]


def newtonian_force(r: float, m1: float, m2: float, G: float = 1.0) -> float:
    return G * m1 * m2 / (r * r)


def yukawa_force(r: float, m1: float, m2: float, G: float = 1.0, alpha: float = 1.0, lambda_s: float = 1.0) -> float:
    return newtonian_force(r, m1, m2, G) * (1 + alpha * (1 + r / lambda_s) * math.exp(-r / lambda_s))


def nfw_g_enhancement(r: float, r_c: float, gamma: float = 1.0) -> float:
    return 1.0 + gamma / (1.0 + (r_c / max(r, 1e-12)) ** 2)


def modified_acceleration(pos_i: Vec, pos_j: Vec, mass_j: float, G: float = 1.0, model: str = "yukawa", alpha: float = 0.5, lambda_s: float = 1.0) -> Vec:
    rvec = [pos_j[d] - pos_i[d] for d in range(len(pos_i))]
    r = math.sqrt(sum(x * x for x in rvec)) + 1e-30
    if model == "yukawa":
        f = yukawa_force(r, 1.0, mass_j, G, alpha, lambda_s)
    else:
        f = newtonian_force(r, 1.0, mass_j, G) * nfw_g_enhancement(r, lambda_s, alpha)
    return [f * rvec[d] / r for d in range(len(rvec))]


if __name__ == "__main__":
    fn = newtonian_force(1.0, 1.0, 1.0)
    fy = yukawa_force(1.0, 1.0, 1.0, alpha=1.0, lambda_s=1.0)
    assert fy > fn
    print(f"modified_gravity F_N={fn:.3f} F_Y={fy:.3f}")
    print("modified_gravity self-tests passed")
