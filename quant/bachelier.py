"""
Universe Simulator - Bachelier (Normal) Model Option Pricing
Original closed-form for futures options under normal dynamics.
"""

from __future__ import annotations

import math

def _norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)

def bachelier_call(F: float, K: float, T: float, sigma: float) -> float:
    if T <= 0 or sigma <= 0:
        return max(F - K, 0.0)
    d = (F - K) / (sigma * math.sqrt(T))
    return (F - K) * _norm_cdf(d) + sigma * math.sqrt(T) * _norm_pdf(d)

def bachelier_put(F: float, K: float, T: float, sigma: float) -> float:
    if T <= 0 or sigma <= 0:
        return max(K - F, 0.0)
    d = (F - K) / (sigma * math.sqrt(T))
    return (K - F) * _norm_cdf(-d) + sigma * math.sqrt(T) * _norm_pdf(d)

if __name__ == "__main__":
    c = bachelier_call(100, 100, 1.0, 20)
    p = bachelier_put(100, 100, 1.0, 20)
    assert abs(c - p) < 1e-6  # ATM parity
    assert c > 0
    print("bachelier self-test passed", c)
