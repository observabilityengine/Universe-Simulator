"""Stationarity checks and transforms."""
from __future__ import annotations
from typing import List
from .adfuller import adfuller
from .arima import difference


def is_stationary(series: List[float], alpha: float = 0.05) -> bool:
    _, p = adfuller(series)
    return p <= alpha


def make_stationary(series: List[float], max_d: int = 2) -> tuple:
    s = list(series)
    d = 0
    for d in range(max_d + 1):
        if is_stationary(s):
            return s, d
        s = difference(s, 1)
    return s, max_d


if __name__ == "__main__":
    s = list(range(50))
    st, d = make_stationary(s)
    assert d >= 1
    print(f"stationarity d={d}")
    print("stationarity self-tests passed")
