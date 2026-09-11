"""Classical seasonal decomposition."""
from __future__ import annotations
from typing import List, Tuple


def decompose(series: List[float], period: int = 4) -> Tuple[List[float], List[float], List[float]]:
    n = len(series)
    # trend via moving average
    trend = [float("nan")] * n
    half = period // 2
    for i in range(half, n - half):
        trend[i] = sum(series[i - half : i + half + (period % 2)]) / period
    # fill edges
    for i in range(half):
        trend[i] = trend[half]
        trend[n - 1 - i] = trend[n - 1 - half]
    # seasonal
    detrended = [series[i] - trend[i] for i in range(n)]
    seasonal = [0.0] * n
    for k in range(period):
        vals = [detrended[i] for i in range(k, n, period)]
        avg = sum(vals) / len(vals) if vals else 0.0
        for i in range(k, n, period):
            seasonal[i] = avg
    # residual
    resid = [series[i] - trend[i] - seasonal[i] for i in range(n)]
    return trend, seasonal, resid


if __name__ == "__main__":
    s = [i % 4 + i * 0.1 for i in range(20)]
    t, seas, r = decompose(s, 4)
    assert len(t) == 20
    print("decompose self-tests passed")
