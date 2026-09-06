"""Ordinary least squares linear regression (closed-form normal equations).

Complexity: O(n d^2 + d^3) for n samples, d features.
Solves min ||Xw - y||^2 with optional intercept column.
Original implementation using NumPy.
"""
from __future__ import annotations

import numpy as np
from typing import Tuple


def linear_regression_fit(
    X: np.ndarray,
    y: np.ndarray,
    fit_intercept: bool = True,
) -> Tuple[np.ndarray, float]:
    """Return (weights, intercept). intercept is 0 if fit_intercept=False."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float).ravel()
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    n, d = X.shape
    if y.shape[0] != n:
        raise ValueError("X and y length mismatch")
    if fit_intercept:
        X_design = np.column_stack([np.ones(n), X])
    else:
        X_design = X
    # normal equations with mild ridge for stability
    xtx = X_design.T @ X_design
    xty = X_design.T @ y
    try:
        coef = np.linalg.solve(xtx, xty)
    except np.linalg.LinAlgError:
        coef = np.linalg.lstsq(X_design, y, rcond=None)[0]
    if fit_intercept:
        return coef[1:], float(coef[0])
    return coef, 0.0


def linear_regression_predict(
    X: np.ndarray, weights: np.ndarray, intercept: float = 0.0
) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    return X @ weights + intercept


if __name__ == "__main__":
    # y = 2x + 1
    X = np.array([[1.0], [2.0], [3.0], [4.0]])
    y = np.array([3.0, 5.0, 7.0, 9.0])
    w, b = linear_regression_fit(X, y)
    assert abs(w[0] - 2.0) < 1e-8 and abs(b - 1.0) < 1e-8
    pred = linear_regression_predict(X, w, b)
    assert np.allclose(pred, y)
    w2, b2 = linear_regression_fit(X, y, fit_intercept=False)
    assert b2 == 0.0
    print("linear_regression_closed self-tests passed")
