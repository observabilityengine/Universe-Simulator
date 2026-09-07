"""Cox-Ross-Rubinstein binomial option pricing.

Complexity: O(n^2) for n steps. Original implementation.
"""
from __future__ import annotations

import math
from typing import Literal


def binomial_option(
    S: float, K: float, T: float, r: float, sigma: float,
    n: int = 100, option: Literal["call", "put"] = "call",
    style: Literal["european", "american"] = "european",
) -> float:
    dt = T / n
    u = math.exp(sigma * math.sqrt(dt))
    d = 1.0 / u
    p = (math.exp(r * dt) - d) / (u - d)
    discount = math.exp(-r * dt)
    values = []
    for j in range(n + 1):
        ST = S * (u ** (n - j)) * (d ** j)
        if option == "call":
            values.append(max(ST - K, 0.0))
        else:
            values.append(max(K - ST, 0.0))
    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            cont = discount * (p * values[j] + (1 - p) * values[j + 1])
            if style == "american":
                ST = S * (u ** (i - j)) * (d ** j)
                exercise = max(ST - K, 0.0) if option == "call" else max(K - ST, 0.0)
                values[j] = max(cont, exercise)
            else:
                values[j] = cont
    return values[0]


if __name__ == "__main__":
    price = binomial_option(100, 100, 1.0, 0.05, 0.2, n=200, option="call")
    assert 8.0 < price < 12.0, price
    put = binomial_option(100, 100, 1.0, 0.05, 0.2, n=200, option="put")
    parity = price - put
    expected = 100 - 100 * math.exp(-0.05)
    assert abs(parity - expected) < 0.5, (parity, expected)
    print("binomial_option self-tests passed")
