"""Ackermann pole-placement for single-input controllable linear systems.

Complexity: O(n^3). Original implementation.
"""
from __future__ import annotations
from typing import List


def _poly_from_poles(poles: List[float]) -> List[float]:
    """Return monic coeffs highest-degree-first: [1, a_{n-1}, ..., a0] for prod (s - r)."""
    # Build low-to-high then reverse
    p = [1.0]  # a0 = 1
    for r in poles:
        # multiply by (s - r): low-to-high
        new_p = [0.0] * (len(p) + 1)
        for i, c in enumerate(p):
            new_p[i] += -r * c
            new_p[i + 1] += c
        p = new_p
    return list(reversed(p))


def pole_placement(A: List[List[float]], B: List[float], poles: List[float]) -> List[float]:
    """Return state-feedback gain K such that eig(A - B K) = poles (Ackermann)."""
    n = len(A)
    assert len(B) == n and len(poles) == n

    # Controllability matrix C = [B, AB, A^2 B, ...]
    ctrb = [[0.0] * n for _ in range(n)]
    v = B[:]
    for col in range(n):
        for i in range(n):
            ctrb[i][col] = v[i]
        # v = A v
        v = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]

    # Invert controllability matrix (Gaussian)
    M = [ctrb[i][:] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[pivot] = M[pivot], M[col]
        piv = M[col][col]
        if abs(piv) < 1e-14:
            raise ValueError("System not controllable")
        for j in range(col, 2 * n):
            M[col][j] /= piv
        for r in range(n):
            if r == col:
                continue
            factor = M[r][col]
            for j in range(col, 2 * n):
                M[r][j] -= factor * M[col][j]
    inv_ctrb = [[M[i][n + j] for j in range(n)] for i in range(n)]

    # Desired characteristic polynomial
    alpha = _poly_from_poles(poles)  # alpha[0]=1, alpha[1] = -sum poles, ...
    # phi(A) = A^n + a_{n-1} A^{n-1} + ... + a0 I
    # Compute powers of A
    Apow = [[[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]]  # I
    for p in range(1, n + 1):
        prev = Apow[-1]
        nxt = [[sum(A[i][k] * prev[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        Apow.append(nxt)

    phiA = [[0.0] * n for _ in range(n)]
    # alpha has length n+1, alpha[0]=1 for A^n, alpha[-1]=a0
    for k in range(n + 1):
        coef = alpha[k]
        for i in range(n):
            for j in range(n):
                phiA[i][j] += coef * Apow[n - k][i][j]

    # K = e_n^T * inv(ctrb) * phi(A)
    # first compute inv_ctrb @ phiA
    M = [[sum(inv_ctrb[i][k] * phiA[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    # then last row
    K = M[-1][:]
    return K


if __name__ == "__main__":
    # Double integrator
    A = [[0.0, 1.0], [0.0, 0.0]]
    B = [0.0, 1.0]
    poles = [-2.0, -3.0]
    K = pole_placement(A, B, poles)
    # Closed-loop A - B K should have those poles
    # Characteristic poly of closed loop: s^2 + (k1)s? wait K=[k1,k2] -> A-BK = [[0,1],[-k1,-k2]]
    # Desired (s+2)(s+3)=s^2+5s+6 -> K should be [6,5]
    assert abs(K[0] - 6.0) < 1e-6
    assert abs(K[1] - 5.0) < 1e-6
    print(f"pole_placement K={K}")
    print("pole_placement self-tests passed")
