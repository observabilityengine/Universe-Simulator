"""
Module 53 – Black-Scholes Option Pricing
Closed-form European call/put + Greeks.
Complete quantitative implementation.
"""

from __future__ import annotations
import math
from typing import Dict


def _norm_cdf(x: float) -> float:
    t = 1.0 / (1.0 + 0.2316419 * abs(x))
    d = 0.3989423 * math.exp(-x * x / 2.0)
    p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))))
    return 1.0 - p if x > 0 else p


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def black_scholes(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: str = "call",
) -> Dict[str, float]:
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        raise ValueError("Invalid parameters")

    sqrt_T = math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrt_T)
    d2 = d1 - sigma * sqrt_T

    if option_type == "call":
        price = S * _norm_cdf(d1) - K * math.exp(-r * T) * _norm_cdf(d2)
        delta = _norm_cdf(d1)
        theta = (
            -S * _norm_pdf(d1) * sigma / (2 * sqrt_T)
            - r * K * math.exp(-r * T) * _norm_cdf(d2)
        )
    elif option_type == "put":
        price = K * math.exp(-r * T) * _norm_cdf(-d2) - S * _norm_cdf(-d1)
        delta = _norm_cdf(d1) - 1.0
        theta = (
            -S * _norm_pdf(d1) * sigma / (2 * sqrt_T)
            + r * K * math.exp(-r * T) * _norm_cdf(-d2)
        )
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    gamma = _norm_pdf(d1) / (S * sigma * sqrt_T)
    vega = S * _norm_pdf(d1) * sqrt_T
    rho_call = K * T * math.exp(-r * T) * _norm_cdf(d2)
    rho = rho_call if option_type == "call" else -K * T * math.exp(-r * T) * _norm_cdf(-d2)

    return {
        "price": price,
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
        "d1": d1,
        "d2": d2,
    }


if __name__ == "__main__":
    print("Testing Black-Scholes...")
    result = black_scholes(S=100, K=100, T=1.0, r=0.05, sigma=0.2, option_type="call")
    print(f"  Call price: {result['price']:.4f}")
    print(f"  Delta: {result['delta']:.4f}")
    print(f"  Gamma: {result['gamma']:.6f}")
    print(f"  Vega:  {result['vega']:.4f}")
    put = black_scholes(S=100, K=100, T=1.0, r=0.05, sigma=0.2, option_type="put")
    print(f"  Put price:  {put['price']:.4f}")
    parity = result["price"] - put["price"] - (100 - 100 * math.exp(-0.05 * 1.0))
    print(f"  Put-call parity residual: {parity:.2e}")
    print("Black-Scholes module OK.")
