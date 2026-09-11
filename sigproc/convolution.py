"""1-D discrete convolution."""
from __future__ import annotations
from typing import List


def convolve(a: List[float], b: List[float]) -> List[float]:
    n, m = len(a), len(b)
    out = [0.0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            out[i + j] += a[i] * b[j]
    return out


if __name__ == "__main__":
    res = convolve([1, 2, 3], [0, 1, 0.5])
    assert abs(res[1] - 1.0) < 1e-9 and abs(res[2] - 2.5) < 1e-9
    print("convolution self-test passed", res)
