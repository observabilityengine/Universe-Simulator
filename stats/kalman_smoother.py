"""
Universe Simulator - Rauch-Tung-Striebel Kalman Smoother (1-D)
Original forward filter + backward smoother.
"""

from __future__ import annotations

from typing import List, Tuple

def rts_smoother(
    observations: List[float],
    q: float = 0.01,
    r: float = 0.1,
    x0: float = 0.0,
    p0: float = 1.0,
) -> List[float]:
    n = len(observations)
    x_filt = [0.0] * n
    p_filt = [0.0] * n
    x_pred = [0.0] * n
    p_pred = [0.0] * n
    x = x0
    p = p0
    for i, z in enumerate(observations):
        x_pred[i] = x
        p_pred[i] = p + q
        k = p_pred[i] / (p_pred[i] + r)
        x = x_pred[i] + k * (z - x_pred[i])
        p = (1 - k) * p_pred[i]
        x_filt[i] = x
        p_filt[i] = p
    # backward
    x_smooth = x_filt[:]
    for i in range(n - 2, -1, -1):
        c = p_filt[i] / p_pred[i + 1]
        x_smooth[i] = x_filt[i] + c * (x_smooth[i + 1] - x_pred[i + 1])
    return x_smooth

if __name__ == "__main__":
    obs = [1.0, 1.1, 0.9, 1.2, 5.0, 1.0, 0.8]
    smooth = rts_smoother(obs)
    assert abs(smooth[4] - 5.0) > abs(smooth[3] - 1.0)  # spike damped relative
    print("kalman_smoother self-test passed", smooth)
