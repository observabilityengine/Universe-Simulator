"""Edit Distance (Levenshtein) with alignment recovery."""
from __future__ import annotations
from typing import Tuple


def levenshtein(a: str, b: str) -> int:
    n, m = len(a), len(b)
    dp = list(range(m + 1))
    for i in range(1, n + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, m + 1):
            temp = dp[j]
            if a[i - 1] == b[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp
    return dp[m]


def levenshtein_alignment(a: str, b: str) -> Tuple[int, str, str]:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    i, j = n, m
    a_aln, b_aln = [], []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else 1):
            a_aln.append(a[i - 1])
            b_aln.append(b[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            a_aln.append(a[i - 1])
            b_aln.append("-")
            i -= 1
        else:
            a_aln.append("-")
            b_aln.append(b[j - 1])
            j -= 1
    return dp[n][m], "".join(reversed(a_aln)), "".join(reversed(b_aln))


if __name__ == "__main__":
    assert levenshtein("kitten", "sitting") == 3
    dist, a_aln, b_aln = levenshtein_alignment("kitten", "sitting")
    assert dist == 3
    print("edit_distance self-tests passed")
