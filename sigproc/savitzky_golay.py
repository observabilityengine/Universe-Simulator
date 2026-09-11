"""Savitzky-Golay filter (quadratic, window 5)."""
from __future__ import annotations
from typing import List


def savgol_smooth(data: List[float]) -> List[float]:
    coeffs = [-3 / 35, 12 / 35, 17 / 35, 12 / 35, -3 / 35]
    n = len(data)
    out = data[:]
    for i in range(2, n - 2):
        out[i] = sum(coeffs[k] * data[i - 2 + k] for k in range(5))
    return out


if __name__ == "__main__":
    noisy = [1.0, 2.1, 2.9, 4.2, 5.0, 5.8, 7.1, 8.0]
    smooth = savgol_smooth(noisy)
    assert abs(smooth[3] - 4.0) < 0.5
    print("savitzky_golay self-test passed", smooth)
