"""Z-score and rolling-IQR anomaly detection."""
from __future__ import annotations
from typing import List, Tuple


def zscore_anomalies(series: List[float], threshold: float = 3.0) -> List[int]:
    n = len(series)
    mean = sum(series) / n
    std = (sum((x - mean) ** 2 for x in series) / n) ** 0.5 or 1.0
    return [i for i, x in enumerate(series) if abs(x - mean) / std > threshold]


def rolling_iqr_anomalies(series: List[float], window: int = 10, k: float = 1.5) -> List[int]:
    anomalies = []
    for i in range(window, len(series)):
        w = sorted(series[i - window : i])
        q1, q3 = w[len(w) // 4], w[3 * len(w) // 4]
        iqr = q3 - q1 or 1.0
        if series[i] < q1 - k * iqr or series[i] > q3 + k * iqr:
            anomalies.append(i)
    return anomalies


if __name__ == "__main__":
    s = [1.0] * 20 + [10.0] + [1.0] * 10
    a = zscore_anomalies(s, 2.0)
    assert 20 in a
    print(f"anomaly_detection {a}")
    print("anomaly_detection self-tests passed")
