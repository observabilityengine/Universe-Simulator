"""Radiative cooling and heating rates – simple metallicity-dependent model."""
from __future__ import annotations
import math


def cooling_rate(T: float, n_H: float, Z: float = 1.0) -> float:
    if T < 1e4:
        lam = 1e-22 * (T / 1e4) ** 0.5
    elif T < 1e5:
        lam = 1e-22 * (T / 1e4) ** (-0.5) * (1 + Z)
    elif T < 1e7:
        lam = 3e-23 * (T / 1e6) ** (-0.7) * (1 + 0.5 * Z)
    else:
        lam = 2e-24 * (T / 1e7) ** 0.5
    return lam * n_H * n_H


def heating_rate(n_H: float, Gamma_UV: float = 1e-25) -> float:
    return Gamma_UV * n_H


def net_cooling(T: float, n_H: float, Z: float = 1.0, Gamma_UV: float = 1e-25) -> float:
    return cooling_rate(T, n_H, Z) - heating_rate(n_H, Gamma_UV)


def equilibrium_temperature(n_H: float, Z: float = 1.0, Gamma_UV: float = 1e-25, T_lo: float = 10.0, T_hi: float = 1e8) -> float:
    for _ in range(60):
        mid = math.sqrt(T_lo * T_hi)
        if net_cooling(mid, n_H, Z, Gamma_UV) > 0:
            T_hi = mid
        else:
            T_lo = mid
    return math.sqrt(T_lo * T_hi)


if __name__ == "__main__":
    lam = cooling_rate(1e6, 1.0)
    assert lam > 0
    Teq = equilibrium_temperature(0.1)
    assert Teq > 0
    print(f"cooling_heating Teq={Teq:.1e}")
    print("cooling_heating self-tests passed")
