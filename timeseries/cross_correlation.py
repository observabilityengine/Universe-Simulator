"""Cross-correlation between two series."""
from __future__ import annotations
from typing import List


def ccf(a: List[float], b: List[float], nlags: int = 10) -> List[float]:
    n = min(len(a), len(b))
    ma, mb = sum(a[:n]) / n, sum(b[:n]) / n
    sa = (sum((x - ma) ** 2 for x in a[:n])) ** 0.5 or 1.0
    sb = (sum((x - mb) ** 2 for x in b[:n])) ** 0.5 or 1.0
    result = []
    for lag in range(-nlags, nlags + 1):
        c = 0.0
        count = 0
        for t in range(n):
            t2 = t + lag
            if 0 <= t2 < n:
                c += (a[t] - ma) * (b[t2] - mb)
                count += 1
        result.append(c / (sa * sb * max(count, 1)))
    return result


if __name__ == "__main__":
    a = [1, 2, 3, 4, 5]
    b = [0, 1, 2, 3, 4]
    c = ccf(a, b, 2)
    assert max(c) > 0.5
    print(f"cross_correlation {c}")
    print("cross_correlation self-tests passed")
