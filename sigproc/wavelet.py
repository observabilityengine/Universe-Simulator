"""Haar discrete wavelet transform (1-D)."""
from __future__ import annotations
from typing import List, Tuple


def haar_forward(x: List[float]) -> Tuple[List[float], List[float]]:
    """One-level Haar: returns (approx, detail). Length must be even."""
    n = len(x)
    if n % 2:
        x = x + [x[-1]]
        n += 1
    s2 = 0.5 ** 0.5
    approx = [(x[i] + x[i + 1]) * s2 for i in range(0, n, 2)]
    detail = [(x[i] - x[i + 1]) * s2 for i in range(0, n, 2)]
    return approx, detail


def haar_inverse(approx: List[float], detail: List[float]) -> List[float]:
    s2 = 0.5 ** 0.5
    out = []
    for a, d in zip(approx, detail):
        out.append((a + d) * s2)
        out.append((a - d) * s2)
    return out


def haar_multilevel(x: List[float], levels: int = 2) -> List[List[float]]:
    coeffs = []
    current = list(x)
    for _ in range(levels):
        if len(current) < 2:
            break
        approx, detail = haar_forward(current)
        coeffs.append(detail)
        current = approx
    coeffs.append(current)
    return coeffs  # [detail_l1, detail_l2, ..., approx]


if __name__ == "__main__":
    x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    a, d = haar_forward(x)
    rec = haar_inverse(a, d)
    assert all(abs(rec[i] - x[i]) < 1e-9 for i in range(len(x)))
    print(f"wavelet approx={a}")
    print("wavelet self-tests passed")
