"""Equation of state library – ideal gas, polytrope, isothermal, degenerate."""
from __future__ import annotations
import math


def ideal_gas(rho: float, T: float, mu: float = 0.6, k_B: float = 1.0, m_H: float = 1.0) -> float:
    return rho * k_B * T / (mu * m_H)


def polytrope(rho: float, K: float, gamma: float) -> float:
    return K * rho ** gamma


def isothermal(rho: float, cs: float) -> float:
    return cs * cs * rho


def degenerate_electron(rho: float, mu_e: float = 2.0) -> float:
    K = 1.0
    return K * (rho / mu_e) ** (5.0 / 3.0)


def sound_speed(P: float, rho: float, gamma: float = 5.0 / 3.0) -> float:
    return math.sqrt(gamma * P / max(rho, 1e-30))


def temperature_from_ideal(P: float, rho: float, mu: float = 0.6, k_B: float = 1.0, m_H: float = 1.0) -> float:
    return P * mu * m_H / (rho * k_B)


if __name__ == "__main__":
    P = ideal_gas(1.0, 10.0)
    assert P > 0
    assert abs(polytrope(2.0, 1.0, 2.0) - 4.0) < 1e-12
    print(f"eos P_ideal={P:.3f}")
    print("eos self-tests passed")
