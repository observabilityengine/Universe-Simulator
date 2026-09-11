"""Savitzky-Golay first derivative (window 5, poly 2)."""
from __future__ import annotations
from typing import List


def savgol_deriv(data: List[float], dt: float = 1.0) -> List[float]:
    # coefficients for first derivative, window=5, poly=2
    coeffs = [-2 / 10, -1 / 10, 0, 1 / 10, 2 / 10]
    n = len(data)
    out = [0.0] * n
    for i in range(2, n - 2):
        out[i] = sum(coeffs[k] * data[i - 2 + k] for k in range(5)) / dt
    return out


if __name__ == "__main__":
    data = [float(i) for i in range(10)]  # slope 1
    d = savgol_deriv(data)
    assert abs(d[5] - 1.0) < 0.2
    print(f"savgol_deriv mid={d[5]:.3f}")
    print("savgol_deriv self-tests passed")
