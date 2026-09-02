"""
Universe Simulator - Black-Scholes Greeks
Original analytic Delta, Gamma, Vega, Theta, Rho.
"""

from __future__ import annotations

import math
from typing import Tuple


def _norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def black_scholes_greeks(
    S: float, K: float, T: float, r: float, sigma: float, option: str = "call"
) -> Tuple[float, float, float, float, float]:
    """Returns (delta, gamma, vega, theta, rho)."""
    if T <= 0 or sigma <= 0:
        raise ValueError("T and sigma must be positive")
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    pdf = _norm_pdf(d1)
    gamma = pdf / (S * sigma * math.sqrt(T))
    vega = S * pdf * math.sqrt(T) / 100  # per 1% 
    if option == "call":
        delta = _norm_cdf(d1)
        theta = (-S * pdf * sigma / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * _norm_cdf(d2)) / 365
        rho = K * T * math.exp(-r * T) * _norm_cdf(d2) / 100
    else:
        delta = _norm_cdf(d1) - 1
        theta = (-S * pdf * sigma / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * _norm_cdf(-d2)) / 365
        rho = -K * T * math.exp(-r * T) * _norm_cdf(-d2) / 100
    return delta, gamma, vega, theta, rho


if __name__ == "__main__":
    d, g, v, t, r = black_scholes_greeks(100, 100, 1.0, 0.05, 0.2, "call")
    assert 0.5 < d < 0.7
    assert g > 0 and v > 0
    print("bs_greeks self-test passed", d, g, v)
