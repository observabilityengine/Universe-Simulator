"""
Universe Simulator - Discrete LQR (finite horizon)
Original dynamic-programming LQR for linear systems.
"""

from __future__ import annotations

from typing import List, Tuple


def discrete_lqr(
    A: List[List[float]],
    B: List[List[float]],
    Q: List[List[float]],
    R: List[List[float]],
    N: int,
) -> List[List[List[float]]]:
    """
    Returns list of feedback gains K_t for t = 0..N-1.
    Assumes 1-D or small systems; pure nested lists.
    """
    n = len(A)
    m = len(B[0]) if B else 0
    P = [row[:] for row in Q]  # terminal cost = Q

    gains = []
    for _ in range(N):
        # K = (R + B^T P B)^-1 B^T P A   (scalar / small matrix inverse)
        # For simplicity this implementation supports scalar (n=1, m=1)
        if n != 1 or m != 1:
            raise NotImplementedError("demo only supports 1-D system")
        BtPB = B[0][0] * P[0][0] * B[0][0]
        inv = 1.0 / (R[0][0] + BtPB)
        K = [[inv * B[0][0] * P[0][0] * A[0][0]]]
        gains.append(K)
        # P = Q + A^T P A - A^T P B K
        APA = A[0][0] * P[0][0] * A[0][0]
        APBK = A[0][0] * P[0][0] * B[0][0] * K[0][0]
        P = [[Q[0][0] + APA - APBK]]
    gains.reverse()
    return gains


if __name__ == "__main__":
    A = [[1.0]]
    B = [[1.0]]
    Q = [[1.0]]
    R = [[0.1]]
    Ks = discrete_lqr(A, B, Q, R, N=5)
    assert len(Ks) == 5
    print("lqr self-test passed", Ks[0])
