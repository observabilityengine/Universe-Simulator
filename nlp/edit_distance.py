"""Levenshtein edit distance."""
from __future__ import annotations


def levenshtein(a: str, b: str) -> int:
    n, m = len(a), len(b)
    dp = list(range(m + 1))
    for i in range(1, n + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, m + 1):
            temp = dp[j]
            if a[i - 1] == b[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp
    return dp[m]


if __name__ == "__main__":
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("abc", "abc") == 0
    print("edit_distance self-tests passed")
