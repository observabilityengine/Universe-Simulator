"""Longest common subsequence (LCS) via dynamic programming.

Complexity: O(m n) time and space for strings of length m, n.
Returns the LCS string (one of possibly many). Original implementation.
"""
from __future__ import annotations


def lcs(a: str, b: str) -> str:
    """Return one longest common subsequence of a and b."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # reconstruct
    i, j = m, n
    chars: list[str] = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            chars.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(chars))


def lcs_length(a: str, b: str) -> int:
    """Return length of LCS only (less memory pressure on reconstruction)."""
    m, n = len(a), len(b)
    if m < n:
        a, b, m, n = b, a, n, m
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[n]


if __name__ == "__main__":
    assert lcs("ABCBDAB", "BDCAB") in ("BCAB", "BDAB")
    assert lcs_length("ABCBDAB", "BDCAB") == 4
    assert lcs("", "abc") == ""
    assert lcs("abc", "") == ""
    assert lcs("abc", "abc") == "abc"
    assert lcs_length("abc", "def") == 0
    print("lcs self-tests passed")
