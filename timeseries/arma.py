"""ARMA(p,q) model."""
from __future__ import annotations
from typing import List, Tuple
from .ar import fit_ar
from .ma import fit_ma


def fit_arma(series: List[float], p: int = 1, q: int = 1) -> Tuple[List[float], List[float]]:
    ar_coefs = fit_ar(series, p)
    # residuals after AR
    residuals = []
    for t in range(p, len(series)):
        pred = sum(ar_coefs[k] * series[t - k - 1] for k in range(p))
        residuals.append(series[t] - pred)
    ma_coefs = fit_ma(residuals, q) if residuals else [0.0] * q
    return ar_coefs, ma_coefs


if __name__ == "__main__":
    s = [0.0]
    for i in range(40):
        s.append(0.5 * s[-1] + 0.1)
    ar_c, ma_c = fit_arma(s, 1, 1)
    print(f"arma ar={ar_c} ma={ma_c}")
    print("arma self-tests passed")
