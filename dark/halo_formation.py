"""Dark matter halo formation – spherical collapse and NFW profile."""
from __future__ import annotations
import math
from typing import Tuple


def spherical_collapse_redshift(delta_i: float, Om: float = 0.3) -> float:
    delta_c = 1.686
    if delta_i <= 0:
        return -1.0
    return max(0.0, delta_c / delta_i - 1.0)


def nfw_density(r: float, rho_s: float, r_s: float) -> float:
    x = r / r_s
    return rho_s / (x * (1 + x) ** 2)


def nfw_mass(r: float, rho_s: float, r_s: float) -> float:
    x = r / r_s
    return 4 * math.pi * rho_s * r_s ** 3 * (math.log(1 + x) - x / (1 + x))


def concentration(mass: float, z: float = 0.0) -> float:
    return 10.0 * (mass / 1e12) ** (-0.1) / (1 + z)


def nfw_from_mass_concentration(M_vir: float, c: float, rho_crit: float, delta: float = 200.0) -> Tuple[float, float]:
    R_vir = (3 * M_vir / (4 * math.pi * delta * rho_crit)) ** (1.0 / 3.0)
    r_s = R_vir / c
    f_c = math.log(1 + c) - c / (1 + c)
    rho_s = M_vir / (4 * math.pi * r_s ** 3 * f_c)
    return rho_s, r_s


if __name__ == "__main__":
    zc = spherical_collapse_redshift(0.01)
    assert zc > 0
    rho = nfw_density(0.1, 1.0, 0.05)
    assert rho > 0
    rs, rss = nfw_from_mass_concentration(1e12, 10, 100)
    assert rs > 0
    print(f"halo_formation z_coll={zc:.1f} rho_s={rs:.2e}")
    print("halo_formation self-tests passed")
