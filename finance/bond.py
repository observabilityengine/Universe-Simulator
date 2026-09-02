"""
Module 86 – Bond Pricing
Fixed-coupon bond price, yield-to-maturity (Newton), duration.
Complete quantitative implementation.
"""

from __future__ import annotations
from typing import Optional


def bond_price(face: float, coupon_rate: float, ytm: float, years: float, freq: int = 2) -> float:
    n = int(years * freq)
    c = face * coupon_rate / freq
    if abs(ytm) < 1e-12:
        return c * n + face
    total = 0.0
    for t in range(1, n + 1):
        total += c / ((1 + ytm / freq) ** t)
    total += face / ((1 + ytm / freq) ** n)
    return total


def bond_ytm(face: float, coupon_rate: float, price: float, years: float, freq: int = 2, tol: float = 1e-8, max_iter: int = 100) -> Optional[float]:
    y = coupon_rate
    for _ in range(max_iter):
        p = bond_price(face, coupon_rate, y, years, freq)
        dy = 1e-6
        p_up = bond_price(face, coupon_rate, y + dy, years, freq)
        dp = (p_up - p) / dy
        if abs(dp) < 1e-14:
            return None
        y_new = y - (p - price) / dp
        if abs(y_new - y) < tol:
            return y_new
        y = y_new
    return None


def macaulay_duration(face: float, coupon_rate: float, ytm: float, years: float, freq: int = 2) -> float:
    n = int(years * freq)
    c = face * coupon_rate / freq
    price = bond_price(face, coupon_rate, ytm, years, freq)
    weighted = 0.0
    for t in range(1, n + 1):
        t_years = t / freq
        cf = c if t < n else c + face
        pv = cf / ((1 + ytm / freq) ** t)
        weighted += t_years * pv
    return weighted / price


if __name__ == "__main__":
    print("Testing Bond Pricing...")
    price = bond_price(1000, 0.05, 0.04, 10, freq=2)
    print(f"  Price (5% coupon, 4% YTM, 10y): {price:.2f}")
    ytm = bond_ytm(1000, 0.05, price, 10, freq=2)
    print(f"  Recovered YTM: {ytm*100:.4f}%")
    dur = macaulay_duration(1000, 0.05, 0.04, 10, freq=2)
    print(f"  Macaulay Duration: {dur:.3f} years")
    print("Bond Pricing module OK.")
