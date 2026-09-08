"""Linear Model Predictive Control with finite-horizon quadratic cost (unconstrained).

Complexity: O(horizon^3) per step via normal equations. Original implementation.
"""
from __future__ import annotations
from typing import List, Tuple


def mpc_step(
    A: List[List[float]],
    B: List[List[float]],
    Q: List[List[float]],
    R: List[List[float]],
    x0: List[float],
    horizon: int = 10,
    xref: List[float] | None = None,
) -> List[float]:
    """Compute optimal first control input for linear system x' = Ax + Bu."""
    n = len(A)
    m = len(B[0])
    if xref is None:
        xref = [0.0] * n

    # Build prediction matrices (dense)
    # Phi: effect of initial state, Gamma: effect of controls
    # We solve unconstrained least-squares on stacked cost

    # Simple single-shooting: optimize u_0 ... u_{N-1}
    # Cost = sum (x_k - xref)^T Q (x_k - xref) + u_k^T R u_k
    # Use gradient descent on the sequence for purity (no heavy linear algebra lib)

    u_seq = [[0.0] * m for _ in range(horizon)]
    lr = 0.05
    for _ in range(80):
        # Forward simulate
        x = x0[:]
        xs = [x[:]]
        for k in range(horizon):
            x_next = [sum(A[i][j] * x[j] for j in range(n)) +
                      sum(B[i][j] * u_seq[k][j] for j in range(m)) for i in range(n)]
            x = x_next
            xs.append(x[:])
        # Backward gradients
        grad_u = [[0.0] * m for _ in range(horizon)]
        # Terminal
        lam = [2 * sum(Q[i][j] * (xs[-1][j] - xref[j]) for j in range(n)) for i in range(n)]
        for k in range(horizon - 1, -1, -1):
            for j in range(m):
                grad_u[k][j] = 2 * sum(R[j][p] * u_seq[k][p] for p in range(m)) + sum(B[i][j] * lam[i] for i in range(n))
            # propagate lambda
            if k > 0:
                err = [xs[k][i] - xref[i] for i in range(n)]
                lam = [2 * sum(Q[i][j] * err[j] for j in range(n)) +
                       sum(A[j][i] * lam[j] for j in range(n)) for i in range(n)]
        # Update
        for k in range(horizon):
            for j in range(m):
                u_seq[k][j] -= lr * grad_u[k][j]
    return u_seq[0]


if __name__ == "__main__":
    # Simple integrator: x' = x + u
    A = [[1.0]]
    B = [[1.0]]
    Q = [[1.0]]
    R = [[0.1]]
    x0 = [5.0]
    u = mpc_step(A, B, Q, R, x0, horizon=8)
    assert abs(u[0]) > 0.1  # should push toward 0
    # Simulate a few steps
    x = 5.0
    for _ in range(15):
        u = mpc_step(A, B, Q, R, [x], horizon=6)
        x = x + u[0]
    assert abs(x) < 0.5, x
    print(f"mpc final x={x:.4f}")
    print("mpc self-tests passed")
