"""
Module 37 – Gradient Descent Optimizer
Scalar and multivariate gradient descent with momentum.
Original implementation.
"""

from __future__ import annotations
import numpy as np
from typing import Callable, List, Tuple


def gradient_descent(
    f: Callable[[np.ndarray], float],
    grad: Callable[[np.ndarray], np.ndarray],
    x0: np.ndarray,
    lr: float = 0.1,
    momentum: float = 0.0,
    max_iter: int = 1000,
    tol: float = 1e-8,
) -> Tuple[np.ndarray, List[float]]:
    x = np.array(x0, dtype=float)
    v = np.zeros_like(x)
    history = []
    for i in range(max_iter):
        g = grad(x)
        v = momentum * v - lr * g
        x = x + v
        val = f(x)
        history.append(val)
        if np.linalg.norm(g) < tol:
            break
    return x, history


if __name__ == "__main__":
    print("Testing Gradient Descent...")
    def f(x):
        return (x[0] - 3) ** 2 + (x[1] + 2) ** 2
    def grad(x):
        return np.array([2 * (x[0] - 3), 2 * (x[1] + 2)])
    x_opt, hist = gradient_descent(f, grad, x0=np.array([0.0, 0.0]), lr=0.1, max_iter=100)
    print(f"  Optimum: {x_opt}")
    print(f"  Final value: {hist[-1]:.6e}")
    print("Gradient Descent module OK.")
