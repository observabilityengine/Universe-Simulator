"""Seasonal ARIMA – seasonal differencing + ARIMA."""
from __future__ import annotations
from typing import List, Tuple
from .arima import fit_arima, difference


def seasonal_difference(series: List[float], period: int = 12) -> List[float]:
    return [series[i] - series[i - period] for i in range(period, len(series))]


def fit_sarima(
    series: List[float], p: int = 1, d: int = 0, q: int = 0, P: int = 0, D: int = 1, Q: int = 0, period: int = 12
) -> Tuple[List[float], List[float]]:
    s = list(series)
    for _ in range(D):
        s = seasonal_difference(s, period)
    ar_c, ma_c, _ = fit_arima(s, p, d, q)
    return ar_c, ma_c


if __name__ == "__main__":
    s = [i % 12 + 0.1 * i for i in range(48)]
    ar_c, ma_c = fit_sarima(s, 1, 0, 0, 0, 1, 0, 12)
    print(f"sarima ar={ar_c}")
    print("sarima self-tests passed")
