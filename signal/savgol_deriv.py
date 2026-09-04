"""
Universe Simulator - Savitzky-Golay Derivative
Original quadratic fit for first derivative estimation.
"""

from __future__ import annotations

from typing import List

def savgol_deriv(data: List[float], window: int = 5) -> List[float]:
    # coefficients for window=5, poly=2, deriv=1
    coeffs = [-0.2, -0.1, 0.0, 0.1, 0.2]
    n = len(data)
    out = [0.0] * n
    half = window // 2
    for i in range(half, n - half):
        out[i] = sum(coeffs[k] * data[i - half + k] for k in range(window))
    return out

if __name__ == "__main__":
    data = [i * i for i in range(10)]  # quadratic
    deriv = savgol_deriv(data)
    assert abs(deriv[5] - 10.0) < 1.0  # 2*x at x=5
    print("savgol_deriv self-test passed", deriv[5])
