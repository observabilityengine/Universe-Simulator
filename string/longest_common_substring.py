"""Longest common substring via DP.

Complexity: O(m n) time and space.
Returns one longest contiguous common substring. Original implementation.
"""
from __future__ import annotations


def longest_common_substring(a: str, b: str) -> str:
    """Return one longest common contiguous substring of a and b."""
    m, n = len(a), len(b)
    if m == 0 or n == 0:
        return ""
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    best_len = 0
    best_end = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > best_len:
                    best_len = dp[i][j]
                    best_end = i
            else:
                dp[i][j] = 0
    return a[best_end - best_len : best_end]


if __name__ == "__main__":
    assert longest_common_substring("ABABC", "BABCA") in ("BAB", "ABC")
    assert longest_common_substring("xyz", "abc") == ""
    assert longest_common_substring("", "abc") == ""
    assert longest_common_substring("hello", "hello") == "hello"
    s = longest_common_substring("aaabb", "aab")
    assert s in ("aa", "aab") or len(s) >= 2
    print("longest_common_substring self-tests passed")
