"""Black-Scholes implied volatility via Newton-Raphson.

Complexity: O(iters). Original implementation.
"""
from __future__ import annotations

import math
from typing import Optional


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def bs_call_price(S: float, K: float, T: float, r: float, sigma: float) -> float:
    if T <= 0 or sigma <= 0:
        return max(S - K * math.exp(-r * max(T, 0)), 0.0)
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * _norm_cdf(d1) - K * math.exp(-r * T) * _norm_cdf(d2)


def bs_vega(S: float, K: float, T: float, r: float, sigma: float) -> float:
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    return S * _norm_pdf(d1) * math.sqrt(T)


def implied_vol(
    price: float,
    S: float,
    K: float,
    T: float,
    r: float,
    is_call: bool = True,
    tol: float = 1e-8,
    max_iter: int = 100,
) -> Optional[float]:
    """Newton-Raphson implied volatility. Returns None on failure."""
    if T <= 0:
        return 0.0
    # Convert put to call via parity if needed
    if not is_call:
        price = price + S - K * math.exp(-r * T)
    # Intrinsic lower bound
    intrinsic = max(S - K * math.exp(-r * T), 0.0)
    if price < intrinsic - 1e-10:
        return None
    if abs(price - intrinsic) < 1e-12:
        return 0.0
    sigma = 0.2  # initial guess
    for _ in range(max_iter):
        p = bs_call_price(S, K, T, r, sigma)
        v = bs_vega(S, K, T, r, sigma)
        if v < 1e-15:
            break
        diff = p - price
        if abs(diff) < tol:
            return sigma
        sigma -= diff / v
        if sigma <= 1e-8:
            sigma = 1e-8
        if sigma > 10.0:
            sigma = 10.0
    # Final check
    if abs(bs_call_price(S, K, T, r, sigma) - price) < 1e-4:
        return sigma
    return None


if __name__ == "__main__":
    S, K, T, r, sig = 100.0, 100.0, 1.0, 0.05, 0.25
    price = bs_call_price(S, K, T, r, sig)
    iv = implied_vol(price, S, K, T, r)
    assert iv is not None and abs(iv - sig) < 1e-6
    # Deep ITM low vol
    price2 = bs_call_price(100, 50, 1.0, 0.0, 0.01)
    iv2 = implied_vol(price2, 100, 50, 1.0, 0.0)
    assert iv2 is not None and iv2 < 0.1
    assert implied_vol(0.0, 100, 100, 1.0, 0.05) is None or implied_vol(0.0, 100, 100, 1.0, 0.05) == 0.0
    print("black_scholes_iv self-tests passed")
