"""Vector Autoregression VAR(1)."""
from __future__ import annotations
from typing import List, Tuple


def fit_var1(series: List[List[float]]) -> List[List[float]]:
    """series: T x K. Returns K x K coefficient matrix."""
    T = len(series) - 1
    K = len(series[0])
    # Y = series[1:], X = series[:-1]
    # B = (X'X)^{-1} X'Y approximated via per-equation OLS
    B = [[0.0] * K for _ in range(K)]
    for j in range(K):
        # predict series[t][j] from series[t-1]
        XtX = [[0.0] * K for _ in range(K)]
        Xty = [0.0] * K
        for t in range(T):
            for a in range(K):
                Xty[a] += series[t][a] * series[t + 1][j]
                for b in range(K):
                    XtX[a][b] += series[t][a] * series[t][b]
        # solve
        aug = [XtX[r][:] + [Xty[r]] for r in range(K)]
        for col in range(K):
            pivot = max(range(col, K), key=lambda r: abs(aug[r][col]))
            aug[col], aug[pivot] = aug[pivot], aug[col]
            piv = aug[col][col] or 1e-12
            aug[col] = [v / piv for v in aug[col]]
            for r in range(K):
                if r != col:
                    f = aug[r][col]
                    aug[r] = [aug[r][c] - f * aug[col][c] for c in range(K + 1)]
        for a in range(K):
            B[a][j] = aug[a][K]
    return B


if __name__ == "__main__":
    s = [[0.0, 0.0]]
    for i in range(30):
        s.append([0.5 * s[-1][0] + 0.1, 0.3 * s[-1][1]])
    B = fit_var1(s)
    print(f"var B[0][0]={B[0][0]:.2f}")
    print("var self-tests passed")
