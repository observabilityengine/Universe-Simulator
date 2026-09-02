"""
Module 72 – Binomial Option Pricing Tree
Cox-Ross-Rubinstein European and American option pricer.
Complete quantitative implementation.
"""

from __future__ import annotations
import math
from typing import Literal


def binomial_tree(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    steps: int = 100,
    option_type: Literal["call", "put"] = "call",
    style: Literal["european", "american"] = "european",
) -> float:
    if steps < 1:
        raise ValueError("steps must be >= 1")
    dt = T / steps
    u = math.exp(sigma * math.sqrt(dt))
    d = 1.0 / u
    p = (math.exp(r * dt) - d) / (u - d)
    discount = math.exp(-r * dt)

    prices = [0.0] * (steps + 1)
    for j in range(steps + 1):
        ST = S * (u ** (steps - j)) * (d ** j)
        if option_type == "call":
            prices[j] = max(ST - K, 0.0)
        else:
            prices[j] = max(K - ST, 0.0)

    for i in range(steps - 1, -1, -1):
        for j in range(i + 1):
            cont = discount * (p * prices[j] + (1 - p) * prices[j + 1])
            if style == "american":
                ST = S * (u ** (i - j)) * (d ** j)
                exercise = max(ST - K, 0.0) if option_type == "call" else max(K - ST, 0.0)
                prices[j] = max(cont, exercise)
            else:
                prices[j] = cont

    return prices[0]


if __name__ == "__main__":
    print("Testing Binomial Tree...")
    call_e = binomial_tree(100, 100, 1.0, 0.05, 0.2, steps=200, option_type="call", style="european")
    put_e = binomial_tree(100, 100, 1.0, 0.05, 0.2, steps=200, option_type="put", style="european")
    call_a = binomial_tree(100, 100, 1.0, 0.05, 0.2, steps=200, option_type="call", style="american")
    put_a = binomial_tree(100, 100, 1.0, 0.05, 0.2, steps=200, option_type="put", style="american")
    print(f"  European Call: {call_e:.4f}")
    print(f"  European Put:  {put_e:.4f}")
    print(f"  American Call: {call_a:.4f}")
    print(f"  American Put:  {put_a:.4f}")
    print("Binomial Tree module OK.")
