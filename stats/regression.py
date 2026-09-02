"""
Module 54 – Ordinary Least Squares Regression
Multi-variable OLS with R², residuals, and prediction.
Complete implementation using normal equations.
"""

from __future__ import annotations
import numpy as np
from typing import Optional


class LinearRegression:
    def __init__(self):
        self.coef_: Optional[np.ndarray] = None
        self.intercept_: float = 0.0
        self.r_squared_: float = 0.0

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LinearRegression":
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float).ravel()
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        n, p = X.shape
        X_ = np.column_stack([np.ones(n), X])
        XtX = X_.T @ X_
        Xty = X_.T @ y
        try:
            beta = np.linalg.solve(XtX, Xty)
        except np.linalg.LinAlgError:
            beta = np.linalg.lstsq(X_, y, rcond=None)[0]
        self.intercept_ = float(beta[0])
        self.coef_ = beta[1:]
        y_pred = X_ @ beta
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        self.r_squared_ = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.coef_ is None:
            raise RuntimeError("Model not fitted")
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        return self.intercept_ + X @ self.coef_

    def residuals(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        return np.asarray(y, dtype=float).ravel() - self.predict(X)


if __name__ == "__main__":
    print("Testing Linear Regression...")
    rng = np.random.default_rng(42)
    X = rng.uniform(0, 10, size=(100, 2))
    true_coef = np.array([1.5, -2.0])
    y = 3.0 + X @ true_coef + rng.normal(0, 0.5, 100)
    model = LinearRegression().fit(X, y)
    print(f"  Intercept: {model.intercept_:.4f} (true 3.0)")
    print(f"  Coefs: {model.coef_} (true {true_coef})")
    print(f"  R²: {model.r_squared_:.4f}")
    preds = model.predict(X[:3])
    print(f"  Sample preds: {np.round(preds, 3)}")
    print("Linear Regression module OK.")
