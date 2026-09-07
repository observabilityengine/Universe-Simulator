"""Ordinary least squares linear regression.

Complexity: O(n d^2 + d^3). Original implementation.
"""
from __future__ import annotations

from typing import List, Tuple


def linear_regression(
    X: List[List[float]], y: List[float], fit_intercept: bool = True,
) -> Tuple[List[float], float]:
    n, d = len(X), len(X[0])
    if fit_intercept:
        Xa = [[1.0] + row for row in X]
        d += 1
    else:
        Xa = [row[:] for row in X]
    XtX = [[sum(Xa[k][i] * Xa[k][j] for k in range(n)) for j in range(d)] for i in range(d)]
    Xty = [sum(Xa[k][i] * y[k] for k in range(n)) for i in range(d)]
    M = [XtX[i][:] + [Xty[i]] for i in range(d)]
    for col in range(d):
        piv = max(range(col, d), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        div = M[col][col]
        if abs(div) < 1e-15:
            raise ValueError("Singular design matrix")
        for j in range(d + 1):
            M[col][j] /= div
        for r in range(d):
            if r != col:
                fac = M[r][col]
                for j in range(d + 1):
                    M[r][j] -= fac * M[col][j]
    beta = [M[i][d] for i in range(d)]
    if fit_intercept:
        return beta[1:], beta[0]
    return beta, 0.0


if __name__ == "__main__":
    X = [[float(i)] for i in range(10)]
    y = [2 * i + 3 for i in range(10)]
    coef, intercept = linear_regression(X, y)
    assert abs(coef[0] - 2.0) < 1e-8
    assert abs(intercept - 3.0) < 1e-8
    print("linear_regression self-tests passed")
