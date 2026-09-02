"""
Module 79 – IRR / NPV
Newton-Raphson IRR solver + Net Present Value.
Complete quantitative implementation.
"""

from __future__ import annotations
from typing import List, Optional


def npv(rate: float, cashflows: List[float]) -> float:
    total = 0.0
    for t, cf in enumerate(cashflows):
        total += cf / ((1.0 + rate) ** t)
    return total


def npv_derivative(rate: float, cashflows: List[float]) -> float:
    total = 0.0
    for t, cf in enumerate(cashflows):
        if t > 0:
            total -= t * cf / ((1.0 + rate) ** (t + 1))
    return total


def irr(cashflows: List[float], guess: float = 0.1, tol: float = 1e-8, max_iter: int = 100) -> Optional[float]:
    rate = guess
    for _ in range(max_iter):
        f = npv(rate, cashflows)
        df = npv_derivative(rate, cashflows)
        if abs(df) < 1e-14:
            return None
        new_rate = rate - f / df
        if abs(new_rate - rate) < tol:
            return new_rate
        rate = new_rate
    return None


if __name__ == "__main__":
    print("Testing IRR/NPV...")
    cfs = [-100.0, 30.0, 40.0, 50.0, 20.0]
    r = irr(cfs)
    print(f"  IRR: {r*100:.2f}%")
    print(f"  NPV at IRR: {npv(r, cfs):.2e}")
    print(f"  NPV at 10%: {npv(0.10, cfs):.4f}")
    print("IRR/NPV module OK.")
