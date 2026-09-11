"""Autocorrelation and partial autocorrelation."""
from __future__ import annotations
from typing import List


def acf(series: List[float], nlags: int = 10) -> List[float]:
    n = len(series)
    mean = sum(series) / n
    var = sum((x - mean) ** 2 for x in series) or 1.0
    result = [1.0]
    for lag in range(1, nlags + 1):
        c = sum((series[t] - mean) * (series[t - lag] - mean) for t in range(lag, n))
        result.append(c / var)
    return result


def pacf(series: List[float], nlags: int = 10) -> List[float]:
    """Durbin-Levinson PACF."""
    acfs = acf(series, nlags)
    pacfs = [1.0]
    if nlags < 1:
        return pacfs
    phi = [[0.0] * (nlags + 1) for _ in range(nlags + 1)]
    phi[1][1] = acfs[1]
    pacfs.append(phi[1][1])
    for k in range(2, nlags + 1):
        num = acfs[k] - sum(phi[k - 1][j] * acfs[k - j] for j in range(1, k))
        den = 1 - sum(phi[k - 1][j] * acfs[j] for j in range(1, k))
        phi[k][k] = num / den if abs(den) > 1e-12 else 0.0
        for j in range(1, k):
            phi[k][j] = phi[k - 1][j] - phi[k][k] * phi[k - 1][k - j]
        pacfs.append(phi[k][k])
    return pacfs


if __name__ == "__main__":
    s = [0.0]
    for i in range(50):
        s.append(0.7 * s[-1])
    a = acf(s, 5)
    assert a[1] > 0.5
    print(f"acf_pacf acf={a[:3]}")
    print("acf_pacf self-tests passed")
