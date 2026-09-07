"""Black-Scholes European option pricing and Greeks.

Complexity: O(1). Original implementation.
"""
from __future__ import annotations

import math
from typing import Tuple


def _norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def black_scholes(
    S: float, K: float, T: float, r: float, sigma: float, option: str = "call",
) -> float:
    if T <= 0:
        return max(S - K, 0.0) if option == "call" else max(K - S, 0.0)
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option == "call":
        return S * _norm_cdf(d1) - K * math.exp(-r * T) * _norm_cdf(d2)
    return K * math.exp(-r * T) * _norm_cdf(-d2) - S * _norm_cdf(-d1)


def black_scholes_greeks(
    S: float, K: float, T: float, r: float, sigma: float,
) -> Tuple[float, float, float, float]:
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    delta = _norm_cdf(d1)
    gamma = _norm_pdf(d1) / (S * sigma * math.sqrt(T))
    vega = S * _norm_pdf(d1) * math.sqrt(T)
    theta = (-S * _norm_pdf(d1) * sigma / (2 * math.sqrt(T))
             - r * K * math.exp(-r * T) * _norm_cdf(d2))
    return delta, gamma, vega, theta


if __name__ == "__main__":
    call = black_scholes(100, 100, 1.0, 0.05, 0.2, "call")
    put = black_scholes(100, 100, 1.0, 0.05, 0.2, "put")
    assert 8 < call < 12
    assert abs((call - put) - (100 - 100 * math.exp(-0.05))) < 1e-6
    delta, gamma, vega, theta = black_scholes_greeks(100, 100, 1.0, 0.05, 0.2)
    assert 0.5 < delta < 0.7
    assert gamma > 0
    print("black_scholes self-tests passed")
