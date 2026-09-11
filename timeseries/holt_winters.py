"""Holt-Winters additive seasonal smoothing."""
from __future__ import annotations
from typing import List, Tuple


def holt_winters(
    series: List[float],
    period: int = 4,
    alpha: float = 0.3,
    beta: float = 0.1,
    gamma: float = 0.1,
) -> Tuple[List[float], float, float, List[float]]:
    n = len(series)
    level = series[0]
    trend = (series[period] - series[0]) / period if n > period else 0.0
    season = [0.0] * period
    for i in range(period):
        season[i] = series[i] - level
    fitted = []
    for t in range(n):
        s = season[t % period]
        fitted.append(level + trend + s)
        if t < n:
            x = series[t]
            new_level = alpha * (x - s) + (1 - alpha) * (level + trend)
            new_trend = beta * (new_level - level) + (1 - beta) * trend
            season[t % period] = gamma * (x - new_level) + (1 - gamma) * s
            level, trend = new_level, new_trend
    return fitted, level, trend, season


if __name__ == "__main__":
    s = [i % 4 + 0.1 * i for i in range(20)]
    fitted, _, _, _ = holt_winters(s, 4)
    assert len(fitted) == 20
    print("holt_winters self-tests passed")
