"""Atmospheric escape – Jeans, hydrodynamic, and energy-limited regimes."""
from __future__ import annotations
import math


def jeans_escape_rate(mass_planet: float, radius: float, T_exosphere: float, n_exobase: float, m_particle: float, G: float = 1.0, k_B: float = 1.0) -> float:
    v_esc = math.sqrt(2 * G * mass_planet / radius)
    v_th = math.sqrt(2 * k_B * T_exosphere / m_particle)
    lam = (v_esc / v_th) ** 2
    return n_exobase * v_th / (2 * math.sqrt(math.pi)) * (1 + lam) * math.exp(-lam)


def energy_limited_escape(F_xuv: float, radius: float, mass_planet: float, efficiency: float = 0.1, G: float = 1.0) -> float:
    return efficiency * math.pi * radius ** 3 * F_xuv / (G * mass_planet)


def hydrodynamic_criterion(mass_planet: float, radius: float, T: float, m_particle: float, G: float = 1.0, k_B: float = 1.0) -> bool:
    lam = G * mass_planet * m_particle / (k_B * T * radius)
    return lam < 3.0


if __name__ == "__main__":
    j = jeans_escape_rate(1.0, 1.0, 1000.0, 1e10, 1.0)
    assert j >= 0
    e = energy_limited_escape(1.0, 1.0, 1.0)
    assert e > 0
    print(f"atmospheric_escape jeans={j:.3e} energy_lim={e:.3e}")
    print("atmospheric_escape self-tests passed")
