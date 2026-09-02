"""
Module 63 – Mean-Variance Portfolio
Markowitz optimal weights + efficient frontier points.
Complete quantitative implementation.
"""

from __future__ import annotations
import numpy as np
from typing import Tuple


def portfolio_return(weights: np.ndarray, mean_returns: np.ndarray) -> float:
    return float(weights @ mean_returns)


def portfolio_volatility(weights: np.ndarray, cov: np.ndarray) -> float:
    return float(np.sqrt(weights @ cov @ weights))


def min_variance_portfolio(cov: np.ndarray) -> np.ndarray:
    n = cov.shape[0]
    ones = np.ones(n)
    inv = np.linalg.inv(cov)
    w = inv @ ones
    w = w / w.sum()
    return w


def max_sharpe_portfolio(
    mean_returns: np.ndarray,
    cov: np.ndarray,
    risk_free: float = 0.0,
) -> np.ndarray:
    excess = mean_returns - risk_free
    inv = np.linalg.inv(cov)
    w = inv @ excess
    w = w / np.abs(w).sum()
    if w.sum() < 0:
        w = -w
    w = w / w.sum()
    return w


def efficient_frontier(
    mean_returns: np.ndarray,
    cov: np.ndarray,
    n_points: int = 20,
) -> Tuple[np.ndarray, np.ndarray]:
    n = len(mean_returns)
    rets = []
    vols = []
    inv = np.linalg.inv(cov)
    ones = np.ones(n)
    for delta in np.logspace(-1, 2, n_points):
        A = inv @ ones
        B = inv @ mean_returns
        w = B / delta + A
        w = w / w.sum()
        rets.append(portfolio_return(w, mean_returns))
        vols.append(portfolio_volatility(w, cov))
    return np.array(vols), np.array(rets)


if __name__ == "__main__":
    print("Testing Portfolio Optimization...")
    rng = np.random.default_rng(42)
    mean = np.array([0.10, 0.12, 0.07, 0.15])
    X = rng.normal(size=(100, 4))
    cov = np.cov(X, rowvar=False) + np.eye(4) * 0.01
    w_min = min_variance_portfolio(cov)
    w_sharpe = max_sharpe_portfolio(mean, cov, risk_free=0.02)
    print(f"  Min-var weights: {np.round(w_min, 3)}")
    print(f"  Max-Sharpe weights: {np.round(w_sharpe, 3)}")
    print(f"  Min-var vol: {portfolio_volatility(w_min, cov):.4f}")
    print(f"  Max-Sharpe ret: {portfolio_return(w_sharpe, mean):.4f}")
    vols, rets = efficient_frontier(mean, cov, n_points=5)
    print(f"  Frontier vols: {np.round(vols, 3)}")
    print("Portfolio module OK.")
