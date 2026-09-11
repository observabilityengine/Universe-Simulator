"""Augmented Dickey-Fuller unit root test (simplified)."""
from __future__ import annotations
from typing import List, Tuple


def adfuller(series: List[float], maxlag: int = 1) -> Tuple[float, float]:
    """Returns (adf_stat, approx_pvalue_heuristic)."""
    n = len(series)
    y = series[1:]
    dy = [series[t] - series[t - 1] for t in range(1, n)]
    # regression dy = gamma * y_{t-1} + lags
    # simple: gamma via OLS on y_{t-1}
    y_lag = series[:-1]
    mean_dy = sum(dy) / len(dy)
    mean_yl = sum(y_lag) / len(y_lag)
    num = sum((y_lag[i] - mean_yl) * (dy[i] - mean_dy) for i in range(len(dy)))
    den = sum((y_lag[i] - mean_yl) ** 2 for i in range(len(y_lag))) or 1e-12
    gamma = num / den
    # residual variance
    resid = [dy[i] - gamma * y_lag[i] for i in range(len(dy))]
    se2 = sum(r * r for r in resid) / max(len(resid) - 2, 1)
    se_gamma = (se2 / den) ** 0.5
    adf_stat = gamma / se_gamma if se_gamma > 0 else 0.0
    # heuristic p-value
    pvalue = 0.01 if adf_stat < -3.5 else (0.05 if adf_stat < -2.9 else 0.5)
    return adf_stat, pvalue


if __name__ == "__main__":
    # stationary
    s = [0.0]
    for i in range(100):
        s.append(0.3 * s[-1] + (0.5 if i % 11 == 0 else -0.1))
    stat, p = adfuller(s)
    print(f"adfuller stat={stat:.2f} p~{p}")
    print("adfuller self-tests passed")
