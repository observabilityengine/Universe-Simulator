"""Singular Value Decomposition via power iteration + deflation (thin SVD).

Complexity: O(iters * m * n * k). Original implementation for top-k.
"""
from __future__ import annotations
import math
from typing import List, Tuple


def _matvec(A: List[List[float]], v: List[float]) -> List[float]:
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def _matTvec(A: List[List[float]], v: List[float]) -> List[float]:
    n = len(A[0])
    return [sum(A[i][j] * v[i] for i in range(len(A))) for j in range(n)]


def svd_power(
    A: List[List[float]],
    k: int = 2,
    max_iter: int = 100,
    tol: float = 1e-8,
    seed: int = 42,
) -> Tuple[List[List[float]], List[float], List[List[float]]]:
    """Return U (m x k), S (k,), Vt (k x n)."""
    import random
    rng = random.Random(seed)
    m = len(A)
    n = len(A[0])
    # Work copy for deflation
    B = [row[:] for row in A]
    U_cols = []
    S = []
    Vt_rows = []
    for _ in range(k):
        v = [rng.gauss(0, 1) for _ in range(n)]
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        v = [x / norm for x in v]
        for _ in range(max_iter):
            u = _matvec(B, v)
            unorm = math.sqrt(sum(x * x for x in u)) or 1.0
            u = [x / unorm for x in u]
            v_new = _matTvec(B, u)
            vnorm = math.sqrt(sum(x * x for x in v_new)) or 1.0
            v_new = [x / vnorm for x in v_new]
            diff = math.sqrt(sum((v_new[i] - v[i]) ** 2 for i in range(n)))
            v = v_new
            if diff < tol:
                break
        sigma = unorm  # after last u normalization the singular value is the previous unorm roughly
        # Recompute sigma accurately
        Av = _matvec(B, v)
        sigma = math.sqrt(sum(x * x for x in Av))
        u = [x / sigma for x in Av] if sigma > 1e-12 else u
        U_cols.append(u)
        S.append(sigma)
        Vt_rows.append(v)
        # Deflate
        for i in range(m):
            for j in range(n):
                B[i][j] -= sigma * u[i] * v[j]
    U = [[U_cols[j][i] for j in range(k)] for i in range(m)]
    return U, S, Vt_rows


if __name__ == "__main__":
    A = [[3.0, 0.0], [0.0, 2.0], [0.0, 0.0]]
    U, S, Vt = svd_power(A, k=2, max_iter=50)
    assert abs(S[0] - 3.0) < 0.1
    assert abs(S[1] - 2.0) < 0.1
    print(f"svd_power S={S}")
    print("svd_power self-tests passed")
