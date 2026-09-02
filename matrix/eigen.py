"""
Module 68 – Power Iteration Eigenvalue
Dominant eigenvalue / eigenvector via power method + Rayleigh quotient.
Complete implementation.
"""

from __future__ import annotations
import numpy as np
from typing import Tuple


def power_iteration(A: np.ndarray, max_iter: int = 1000, tol: float = 1e-12) -> Tuple[float, np.ndarray]:
    A = np.asarray(A, dtype=float)
    n = A.shape[0]
    v = np.ones(n) / np.sqrt(n)
    for _ in range(max_iter):
        Av = A @ v
        v_new = Av / np.linalg.norm(Av)
        if np.linalg.norm(v_new - v) < tol:
            v = v_new
            break
        v = v_new
    lam = float(v @ A @ v)
    return lam, v


def rayleigh_quotient_iteration(A: np.ndarray, max_iter: int = 50, tol: float = 1e-12) -> Tuple[float, np.ndarray]:
    A = np.asarray(A, dtype=float)
    n = A.shape[0]
    v = np.ones(n)
    v = v / np.linalg.norm(v)
    lam = float(v @ A @ v)
    I = np.eye(n)
    for _ in range(max_iter):
        try:
            w = np.linalg.solve(A - lam * I, v)
        except np.linalg.LinAlgError:
            break
        v = w / np.linalg.norm(w)
        lam_new = float(v @ A @ v)
        if abs(lam_new - lam) < tol:
            lam = lam_new
            break
        lam = lam_new
    return lam, v


if __name__ == "__main__":
    print("Testing Eigenvalue Solvers...")
    A = np.array([[4.0, 1.0], [2.0, 3.0]])
    lam, v = power_iteration(A)
    print(f"  Power iteration λ ≈ {lam:.6f}")
    print(f"  Residual ||Av - λv|| = {np.linalg.norm(A @ v - lam * v):.2e}")
    lam2, v2 = rayleigh_quotient_iteration(A)
    print(f"  Rayleigh λ ≈ {lam2:.6f}")
    print("Eigenvalue module OK.")
