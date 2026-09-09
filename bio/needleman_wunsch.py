"""Needleman-Wunsch global sequence alignment."""
from __future__ import annotations
from typing import Tuple


def needleman_wunsch(a: str, b: str, match: int = 1, mismatch: int = -1, gap: int = -1) -> Tuple[int, str, str]:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = i * gap
    for j in range(1, m + 1):
        dp[0][j] = j * gap
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = match if a[i - 1] == b[j - 1] else mismatch
            dp[i][j] = max(dp[i - 1][j - 1] + s, dp[i - 1][j] + gap, dp[i][j - 1] + gap)
    i, j = n, m
    aa, bb = [], []
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            s = match if a[i - 1] == b[j - 1] else mismatch
            if dp[i][j] == dp[i - 1][j - 1] + s:
                aa.append(a[i - 1])
                bb.append(b[j - 1])
                i -= 1
                j -= 1
                continue
        if i > 0 and dp[i][j] == dp[i - 1][j] + gap:
            aa.append(a[i - 1])
            bb.append("-")
            i -= 1
        else:
            aa.append("-")
            bb.append(b[j - 1])
            j -= 1
    return dp[n][m], "".join(reversed(aa)), "".join(reversed(bb))


if __name__ == "__main__":
    score, aln_a, aln_b = needleman_wunsch("GATTACA", "GCATGCU")
    assert len(aln_a) == len(aln_b)
    print(f"needleman_wunsch score={score} {aln_a}/{aln_b}")
    print("needleman_wunsch self-tests passed")
