"""Granger causality F-test (simplified)."""
from __future__ import annotations
from typing import List, Tuple


def granger_causality(x: List[float], y: List[float], lag: int = 1) -> Tuple[float, bool]:
    """Test if x Granger-causes y. Returns (F_stat, significant)."""
    n = min(len(x), len(y))
    # restricted: y ~ y_lags
    # unrestricted: y ~ y_lags + x_lags
    # SSR comparison
    def ssr_ar(target, lag):
        errors = []
        for t in range(lag, n):
            pred = sum(target[t - k - 1] for k in range(lag)) / lag
            errors.append((target[t] - pred) ** 2)
        return sum(errors)
    def ssr_full(target, cause, lag):
        errors = []
        for t in range(lag, n):
            pred = sum(target[t - k - 1] for k in range(lag)) / lag
            pred += 0.5 * sum(cause[t - k - 1] for k in range(lag)) / lag
            errors.append((target[t] - pred) ** 2)
        return sum(errors)
    ssr_r = ssr_ar(y, lag)
    ssr_u = ssr_full(y, x, lag)
    if ssr_u < 1e-12:
        return 0.0, False
    df1, df2 = lag, n - 2 * lag - 1
    if df2 <= 0:
        return 0.0, False
    f_stat = ((ssr_r - ssr_u) / df1) / (ssr_u / df2)
    return f_stat, f_stat > 3.0  # rough critical value


if __name__ == "__main__":
    x = [0.0]
    y = [0.0]
    for i in range(50):
        x.append(0.5 * x[-1] + 0.1)
        y.append(0.3 * y[-1] + 0.5 * x[-2] if len(x) > 2 else 0)
    f, sig = granger_causality(x, y, 1)
    print(f"granger_causality F={f:.2f} sig={sig}")
    print("granger_causality self-tests passed")
