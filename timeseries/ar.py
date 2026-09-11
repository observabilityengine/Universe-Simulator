"""Autoregressive AR(p) model."""
from __future__ import annotations
from typing import List


def fit_ar(series: List[float], p: int = 1) -> List[float]:
    """Yule-Walker style least squares for AR coefficients."""
    n = len(series)
    if n <= p:
        return [0.0] * p
    # Build design matrix
    y = series[p:]
    X = [[series[i - k - 1] for k in range(p)] for i in range(p, n)]
    # Normal equations XtX beta = Xty
    XtX = [[sum(X[i][a] * X[i][b] for i in range(len(X))) for b in range(p)] for a in range(p)]
    Xty = [sum(X[i][a] * y[i] for i in range(len(X))) for a in range(p)]
    # Gauss-Jordan
    aug = [XtX[r][:] + [Xty[r]] for r in range(p)]
    for col in range(p):
        pivot = max(range(col, p), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        piv = aug[col][col] or 1e-12
        aug[col] = [v / piv for v in aug[col]]
        for r in range(p):
            if r != col:
                f = aug[r][col]
                aug[r] = [aug[r][c] - f * aug[col][c] for c in range(p + 1)]
    return [aug[r][p] for r in range(p)]


def predict_ar(series: List[float], coefs: List[float], steps: int = 1) -> List[float]:
    hist = list(series)
    preds = []
    for _ in range(steps):
        val = sum(coefs[k] * hist[-k - 1] for k in range(len(coefs)) if len(hist) > k)
        preds.append(val)
        hist.append(val)
    return preds


if __name__ == "__main__":
    # AR(1) with phi=0.8
    s = [0.0]
    for i in range(50):
        s.append(0.8 * s[-1] + (0.1 if i % 7 == 0 else 0))
    coefs = fit_ar(s, 1)
    assert abs(coefs[0] - 0.8) < 0.3
    print(f"ar coef={coefs}")
    print("ar self-tests passed")
