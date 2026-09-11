"""Simple exponential smoothing."""
from __future__ import annotations
from typing import List


def ses(series: List[float], alpha: float = 0.3) -> List[float]:
    level = series[0]
    fitted = [level]
    for x in series[1:]:
        level = alpha * x + (1 - alpha) * level
        fitted.append(level)
    return fitted


def forecast_ses(series: List[float], alpha: float = 0.3, steps: int = 1) -> List[float]:
    fitted = ses(series, alpha)
    return [fitted[-1]] * steps


if __name__ == "__main__":
    s = [1, 2, 3, 4, 5]
    f = ses(s, 0.5)
    assert abs(f[-1] - 5) < 2
    print(f"exponential_smoothing {f}")
    print("exponential_smoothing self-tests passed")
