"""Support Vector Machine trained by Sequential Minimal Optimization (SMO).

Binary soft-margin classification. Complexity: O(n^2 * iters). Original.
"""
from __future__ import annotations
import math
import random
from typing import List, Tuple


def linear_kernel(x1: List[float], x2: List[float]) -> float:
    return sum(a * b for a, b in zip(x1, x2))


def smo_train(
    X: List[List[float]],
    y: List[int],
    C: float = 1.0,
    tol: float = 1e-3,
    max_passes: int = 20,
    seed: int = 42,
) -> Tuple[List[float], float]:
    """Returns alphas and bias b. Decision: sum alpha_i y_i K(x_i, x) + b."""
    rng = random.Random(seed)
    n = len(X)
    alphas = [0.0] * n
    b = 0.0
    passes = 0
    while passes < max_passes:
        num_changed = 0
        for i in range(n):
            # Compute error
            Ei = sum(alphas[j] * y[j] * linear_kernel(X[j], X[i]) for j in range(n)) + b - y[i]
            if (y[i] * Ei < -tol and alphas[i] < C) or (y[i] * Ei > tol and alphas[i] > 0):
                j = i
                while j == i:
                    j = rng.randrange(n)
                Ej = sum(alphas[k] * y[k] * linear_kernel(X[k], X[j]) for k in range(n)) + b - y[j]
                ai_old, aj_old = alphas[i], alphas[j]
                if y[i] != y[j]:
                    L = max(0.0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0.0, alphas[i] + alphas[j] - C)
                    H = min(C, alphas[i] + alphas[j])
                if abs(L - H) < 1e-12:
                    continue
                eta = 2 * linear_kernel(X[i], X[j]) - linear_kernel(X[i], X[i]) - linear_kernel(X[j], X[j])
                if eta >= 0:
                    continue
                alphas[j] = aj_old - y[j] * (Ei - Ej) / eta
                alphas[j] = max(L, min(H, alphas[j]))
                if abs(alphas[j] - aj_old) < 1e-5:
                    continue
                alphas[i] = ai_old + y[i] * y[j] * (aj_old - alphas[j])
                # Update bias
                b1 = b - Ei - y[i] * (alphas[i] - ai_old) * linear_kernel(X[i], X[i]) - \
                     y[j] * (alphas[j] - aj_old) * linear_kernel(X[i], X[j])
                b2 = b - Ej - y[i] * (alphas[i] - ai_old) * linear_kernel(X[i], X[j]) - \
                     y[j] * (alphas[j] - aj_old) * linear_kernel(X[j], X[j])
                if 0 < alphas[i] < C:
                    b = b1
                elif 0 < alphas[j] < C:
                    b = b2
                else:
                    b = 0.5 * (b1 + b2)
                num_changed += 1
        if num_changed == 0:
            passes += 1
        else:
            passes = 0
    return alphas, b


def predict(alphas: List[float], b: float, X: List[List[float]], y: List[int], x: List[float]) -> int:
    val = sum(alphas[i] * y[i] * linear_kernel(X[i], x) for i in range(len(X))) + b
    return 1 if val >= 0 else -1


if __name__ == "__main__":
    # Simple linearly separable
    X = [[0.0, 0.0], [1.0, 1.0], [0.5, 0.3], [2.0, 2.5], [1.8, 1.9], [0.1, 0.2]]
    y = [-1, 1, -1, 1, 1, -1]
    alphas, b = smo_train(X, y, C=10.0, max_passes=30, seed=1)
    correct = sum(1 for i in range(len(X)) if predict(alphas, b, X, y, X[i]) == y[i])
    assert correct >= 5, correct
    print(f"svm_smo accuracy={correct}/{len(X)}")
    print("svm_smo self-tests passed")
