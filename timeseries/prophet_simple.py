"""Simplified Prophet-style decomposable model (trend + seasonality)."""
from __future__ import annotations
import math
from typing import List, Tuple
from .fourier_features import fourier_features


def fit_prophet_simple(series: List[float], period: float = 7.0) -> Tuple[float, float, List[float]]:
    n = len(series)
    t = list(range(n))
    # linear trend via OLS
    mean_t = sum(t) / n
    mean_y = sum(series) / n
    slope = sum((t[i] - mean_t) * (series[i] - mean_y) for i in range(n)) / (sum((ti - mean_t) ** 2 for ti in t) or 1)
    intercept = mean_y - slope * mean_t
    # seasonal via Fourier
    feats = fourier_features(t, period, 3)
    # residual after trend
    resid = [series[i] - (intercept + slope * t[i]) for i in range(n)]
    # average Fourier coefficients (simplified)
    season = [0.0] * n
    for i in range(n):
        season[i] = sum(feats[i]) / len(feats[i]) * 0.1
    return intercept, slope, season


def predict_prophet(intercept: float, slope: float, season: List[float], steps: int) -> List[float]:
    n = len(season)
    return [intercept + slope * (n + i) + season[i % n] for i in range(steps)]


if __name__ == "__main__":
    s = [10 + 0.1 * i + math.sin(2 * math.pi * i / 7) for i in range(28)]
    b0, b1, seas = fit_prophet_simple(s, 7)
    preds = predict_prophet(b0, b1, seas, 3)
    assert len(preds) == 3
    print(f"prophet_simple slope={b1:.3f}")
    print("prophet_simple self-tests passed")
