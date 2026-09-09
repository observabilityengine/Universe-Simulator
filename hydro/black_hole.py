"""Black hole physics – Schwarzschild, ISCO, accretion, Hawking temperature, Kerr spin."""
from __future__ import annotations
import math

G = 1.0
C = 1.0
HBAR = 1.0
K_B = 1.0


def schwarzschild_radius(mass: float) -> float:
    return 2 * G * mass / (C * C)


def isco_radius(mass: float, spin: float = 0.0) -> float:
    a = max(-0.999, min(0.999, spin))
    Z1 = 1 + (1 - a * a) ** (1 / 3) * ((1 + a) ** (1 / 3) + (1 - a) ** (1 / 3))
    Z2 = math.sqrt(3 * a * a + Z1 * Z1)
    r_isco = 3 + Z2 - math.copysign(1, a) * math.sqrt((3 - Z1) * (3 + Z1 + 2 * Z2))
    return r_isco * G * mass / (C * C)


def hawking_temperature(mass: float) -> float:
    return HBAR * C ** 3 / (8 * math.pi * G * mass * K_B)


def eddington_luminosity(mass: float, kappa: float = 0.4) -> float:
    return 4 * math.pi * G * mass * C / kappa


def bondi_accretion_rate(mass: float, rho_inf: float, cs_inf: float) -> float:
    lam = 1.0
    return 4 * math.pi * lam * (G * mass) ** 2 * rho_inf / (cs_inf ** 3)


if __name__ == "__main__":
    rs = schwarzschild_radius(1.0)
    assert abs(rs - 2.0) < 1e-12
    assert isco_radius(1.0, 0.0) > rs
    T = hawking_temperature(1.0)
    assert T > 0
    print(f"black_hole rs={rs} ISCO={isco_radius(1):.3f} T_H={T:.3e}")
    print("black_hole self-tests passed")
