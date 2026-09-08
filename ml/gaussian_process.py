"""Gaussian Process regression with RBF kernel and exact inference.

Complexity: O(n^3) for train, O(n^2) predict. Original implementation.
"""
from __future__ import annotations
import math
from typing import List, Tuple


def rbf_kernel(x1: List[float], x2: List[float], length: float = 1.0, sigma_f: float = 1.0) -> float:
    s = sum((a - b) ** 2 for a, b in zip(x1, x2))
    return sigma_f * sigma_f * math.exp(-0.5 * s / (length * length))


def gp_train(
    X: List[List[float]],
    y: List[float],
    length: float = 1.0,
    sigma_f: float = 1.0,
    noise: float = 1e-6,
) -> Tuple[List[List[float]], List[float], List[List[float]]]:
    n = len(X)
    K = [[rbf_kernel(X[i], X[j], length, sigma_f) + (noise if i == j else 0.0)
          for j in range(n)] for i in range(n)]
    # Cholesky
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                L[i][j] = math.sqrt(max(K[i][i] - s, 1e-18))
            else:
                L[i][j] = (K[i][j] - s) / L[j][j]
    # Solve L alpha = y, then L^T alpha = alpha
    alpha = y[:]
    for i in range(n):
        alpha[i] = (alpha[i] - sum(L[i][k] * alpha[k] for k in range(i))) / L[i][i]
    for i in range(n - 1, -1, -1):
        alpha[i] = (alpha[i] - sum(L[k][i] * alpha[k] for k in range(i + 1, n))) / L[i][i]
    return L, alpha, X


def gp_predict(
    L: List[List[float]],
    alpha: List[float],
    X_train: List[List[float]],
    x_star: List[float],
    length: float = 1.0,
    sigma_f: float = 1.0,
) -> Tuple[float, float]:
    n = len(X_train)
    k_star = [rbf_kernel(x_star, X_train[i], length, sigma_f) for i in range(n)]
    mean = sum(k_star[i] * alpha[i] for i in range(n))
    # variance
    v = k_star[:]
    for i in range(n):
        v[i] = (v[i] - sum(L[i][k] * v[k] for k in range(i))) / L[i][i]
    var = sigma_f * sigma_f - sum(vi * vi for vi in v)
    return mean, max(var, 0.0)


if __name__ == "__main__":
    # Fit y = sin(x)
    X = [[float(i) * 0.5] for i in range(10)]
    y = [math.sin(x[0]) for x in X]
    L, alpha, Xt = gp_train(X, y, length=0.8, noise=1e-5)
    mu, var = gp_predict(L, alpha, Xt, [1.2], length=0.8)
    true = math.sin(1.2)
    assert abs(mu - true) < 0.15, (mu, true)
    assert var >= 0.0
    print(f"gp pred={mu:.4f} true={true:.4f} var={var:.4f}")
    print("gaussian_process self-tests passed")
