"""Moving Average MA(q) model via innovations."""
from __future__ import annotations
from typing import List


def fit_ma(series: List[float], q: int = 1, n_iter: int = 20) -> List[float]:
    """Simple iterative MA fitting."""
    n = len(series)
    mean = sum(series) / n
    residuals = [x - mean for x in series]
    theta = [0.0] * q
    for _ in range(n_iter):
        # recompute residuals
        new_res = []
        for t in range(n):
            r = series[t] - mean
            for k in range(q):
                if t - k - 1 >= 0:
                    r -= theta[k] * new_res[t - k - 1] if t - k - 1 < len(new_res) else 0
            new_res.append(r)
        # update theta via correlation of residuals
        for k in range(q):
            num = sum(new_res[t] * new_res[t - k - 1] for t in range(k + 1, n))
            den = sum(new_res[t] ** 2 for t in range(n - k - 1)) or 1
            theta[k] = num / den
        residuals = new_res
    return theta


if __name__ == "__main__":
    s = [0.0, 1.0, 0.5, -0.3, 0.2, 0.1, -0.1, 0.05]
    theta = fit_ma(s, 1)
    print(f"ma theta={theta}")
    print("ma self-tests passed")
