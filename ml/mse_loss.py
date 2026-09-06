"""Mean squared error and mean absolute error losses.

Complexity: O(n).
Original implementation.
"""
from __future__ import annotations

import numpy as np


def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=float).ravel()
    y_pred = np.asarray(y_pred, dtype=float).ravel()
    if y_true.shape != y_pred.shape:
        raise ValueError("shape mismatch")
    if y_true.size == 0:
        return 0.0
    return float(np.mean((y_true - y_pred) ** 2))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=float).ravel()
    y_pred = np.asarray(y_pred, dtype=float).ravel()
    if y_true.shape != y_pred.shape:
        raise ValueError("shape mismatch")
    if y_true.size == 0:
        return 0.0
    return float(np.mean(np.abs(y_true - y_pred)))


if __name__ == "__main__":
    yt = np.array([1.0, 2.0, 3.0])
    yp = np.array([1.0, 2.0, 3.0])
    assert mse(yt, yp) == 0.0
    assert mae(yt, yp) == 0.0
    assert abs(mse(yt, np.array([1.0, 2.0, 5.0])) - 4.0 / 3.0) < 1e-12
    print("mse_loss self-tests passed")
