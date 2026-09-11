"""Longest Common Substring (contiguous)."""
from __future__ import annotations


def longest_common_substring(a: str, b: str) -> str:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    best_len = 0
    best_end = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > best_len:
                    best_len = dp[i][j]
                    best_end = i
            else:
                dp[i][j] = 0
    return a[best_end - best_len : best_end]


if __name__ == "__main__":
    s = longest_common_substring("abcdef", "zbcdf")
    assert s == "bcd"
    print(f"longest_common_substring {s}")
    print("longest_common_substring self-tests passed")
