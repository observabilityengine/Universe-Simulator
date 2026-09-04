"""
Universe Simulator - Lambert W Function (principal branch)
Original Halley iteration for W_0(x).
"""

from __future__ import annotations

import math

def lambert_w(x: float, tol: float = 1e-10, max_iter: int = 50) -> float:
    if x < -1 / math.e:
        raise ValueError("x must be >= -1/e")
    if x == 0:
        return 0.0
    if x < 0:
        w = -1.0 + 1e-6
    else:
        w = math.log(1 + x) if x < 1 else math.log(x)
    for _ in range(max_iter):
        ew = math.exp(w)
        wew = w * ew
        num = wew - x
        den = ew * (w + 1) - (w + 2) * num / (2 * (w + 1))
        delta = num / den
        w -= delta
        if abs(delta) < tol:
            break
    return w

if __name__ == "__main__":
    assert abs(lambert_w(0.0)) < 1e-9
    assert abs(lambert_w(math.e) - 1.0) < 1e-6
    print("lambert_w self-test passed", lambert_w(math.e))
