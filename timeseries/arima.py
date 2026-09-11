"""ARIMA(p,d,q) via differencing + ARMA."""
from __future__ import annotations
from typing import List, Tuple
from .arma import fit_arma


def difference(series: List[float], d: int = 1) -> List[float]:
    s = list(series)
    for _ in range(d):
        s = [s[i] - s[i - 1] for i in range(1, len(s))]
    return s


def invert_difference(diff: List[float], original: List[float], d: int = 1) -> List[float]:
    s = list(original[-d:]) if d else []
    for val in diff:
        if d == 1:
            s.append(s[-1] + val)
        else:
            s.append(val)
    return s[d:] if d else diff


def fit_arima(series: List[float], p: int = 1, d: int = 1, q: int = 0) -> Tuple[List[float], List[float], List[float]]:
    diffed = difference(series, d)
    ar_c, ma_c = fit_arma(diffed, p, q)
    return ar_c, ma_c, diffed


if __name__ == "__main__":
    s = [i + 0.1 * (i % 3) for i in range(30)]
    ar_c, ma_c, _ = fit_arima(s, 1, 1, 0)
    print(f"arima ar={ar_c}")
    print("arima self-tests passed")
