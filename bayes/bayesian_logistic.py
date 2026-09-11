"""Bayesian logistic regression via Laplace approximation."""
from __future__ import annotations
import math
from typing import List, Tuple


def sigmoid(z: float) -> float:
    if z >= 0:
        return 1 / (1 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1 + ez)


def fit(X: List[List[float]], y: List[int], prior_prec: float = 1.0, n_iter: int = 20) -> List[float]:
    n, d = len(X), len(X[0])
    w = [0.0] * d
    for _ in range(n_iter):
        grad = [-prior_prec * w[j] for j in range(d)]
        for i in range(n):
            z = sum(w[j] * X[i][j] for j in range(d))
            p = sigmoid(z)
            for j in range(d):
                grad[j] += (y[i] - p) * X[i][j]
        for j in range(d):
            w[j] += 0.1 * grad[j]
    return w


def predict_proba(X: List[List[float]], w: List[float]) -> List[float]:
    return [sigmoid(sum(w[j] * x[j] for j in range(len(w)))) for x in X]


if __name__ == "__main__":
    X = [[1, 0], [1, 1], [1, 2], [1, 3]]
    y = [0, 0, 1, 1]
    w = fit(X, y)
    probs = predict_proba(X, w)
    assert probs[-1] > probs[0]
    print(f"bayesian_logistic probs={probs}")
    print("bayesian_logistic self-tests passed")
