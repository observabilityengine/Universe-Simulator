"""Bayesian linear regression with known noise variance."""
from __future__ import annotations
from typing import List, Tuple


def fit(X: List[List[float]], y: List[float], prior_prec: float = 1.0, noise_var: float = 1.0) -> Tuple[List[float], List[List[float]]]:
    n, d = len(X), len(X[0])
    # Posterior precision Lambda = prior_prec I + X'X / noise_var
    XtX = [[0.0] * d for _ in range(d)]
    Xty = [0.0] * d
    for i in range(n):
        for j in range(d):
            Xty[j] += X[i][j] * y[i]
            for k in range(d):
                XtX[j][k] += X[i][j] * X[i][k]
    Lambda = [[(XtX[j][k] / noise_var) + (prior_prec if j == k else 0.0) for k in range(d)] for j in range(d)]
    # Solve Lambda mu = Xty / noise_var via Gauss-Jordan
    rhs = [Xty[j] / noise_var for j in range(d)]
    aug = [Lambda[j][:] + [rhs[j]] for j in range(d)]
    for col in range(d):
        pivot = max(range(col, d), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        piv = aug[col][col] or 1e-12
        aug[col] = [v / piv for v in aug[col]]
        for r in range(d):
            if r != col:
                factor = aug[r][col]
                aug[r] = [aug[r][c] - factor * aug[col][c] for c in range(d + 1)]
    mu = [aug[j][d] for j in range(d)]
    return mu, Lambda


if __name__ == "__main__":
    X = [[1, 0], [1, 1], [1, 2], [1, 3]]
    y = [1.0, 2.0, 2.9, 4.1]
    mu, _ = fit(X, y)
    assert abs(mu[1] - 1.0) < 0.3
    print(f"bayesian_linear mu={mu}")
    print("bayesian_linear self-tests passed")
