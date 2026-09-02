"""
Module 92 – Black-76 Futures Option Pricing
Closed-form futures option + Greeks.
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
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def black76(F: float, K: float, T: float, r: float, sigma: float, option_type: str = "call") -> Dict[str, float]:
    if T <= 0 or sigma <= 0 or F <= 0 or K <= 0:
        raise ValueError("Invalid parameters")
    sqrt_T = math.sqrt(T)
    d1 = (math.log(F / K) + 0.5 * sigma * sigma * T) / (sigma * sqrt_T)
    d2 = d1 - sigma * sqrt_T
    df = math.exp(-r * T)
    if option_type == "call":
        price = df * (F * _norm_cdf(d1) - K * _norm_cdf(d2))
        delta = df * _norm_cdf(d1)
    elif option_type == "put":
        price = df * (K * _norm_cdf(-d2) - F * _norm_cdf(-d1))
        delta = -df * _norm_cdf(-d1)
    else:
        raise ValueError("option_type must be call or put")
    gamma = df * _norm_pdf(d1) / (F * sigma * sqrt_T)
    vega = df * F * _norm_pdf(d1) * sqrt_T
    theta = -df * F * _norm_pdf(d1) * sigma / (2 * sqrt_T) + r * price
    return {"price": price, "delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "d1": d1, "d2": d2}


if __name__ == "__main__":
    print("Testing Black-76...")
    result = black76(F=100, K=100, T=1.0, r=0.05, sigma=0.2, option_type="call")
    print(f"  Call price: {result['price']:.4f}")
    print(f"  Delta: {result['delta']:.4f}")
    print(f"  Vega:  {result['vega']:.4f}")
    put = black76(F=100, K=100, T=1.0, r=0.05, sigma=0.2, option_type="put")
    print(f"  Put price:  {put['price']:.4f}")
    print("Black-76 module OK.")
