"""Smith-Waterman local sequence alignment."""
from __future__ import annotations
from typing import Tuple


def smith_waterman(a: str, b: str, match: int = 2, mismatch: int = -1, gap: int = -1) -> Tuple[int, str, str]:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    best, bi, bj = 0, 0, 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = match if a[i - 1] == b[j - 1] else mismatch
            dp[i][j] = max(0, dp[i - 1][j - 1] + s, dp[i - 1][j] + gap, dp[i][j - 1] + gap)
            if dp[i][j] > best:
                best, bi, bj = dp[i][j], i, j
    i, j = bi, bj
    aa, bb = [], []
    while i > 0 and j > 0 and dp[i][j] > 0:
        s = match if a[i - 1] == b[j - 1] else mismatch
        if dp[i][j] == dp[i - 1][j - 1] + s:
            aa.append(a[i - 1])
            bb.append(b[j - 1])
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j] + gap:
            aa.append(a[i - 1])
            bb.append("-")
            i -= 1
        else:
            aa.append("-")
            bb.append(b[j - 1])
            j -= 1
    return best, "".join(reversed(aa)), "".join(reversed(bb))


if __name__ == "__main__":
    score, aa, bb = smith_waterman("GGTTGACTA", "TGTTACGG")
    assert score > 0
    print(f"smith_waterman score={score} {aa}/{bb}")
    print("smith_waterman self-tests passed")
