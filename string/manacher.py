"""
Universe Simulator - Manacher's Algorithm
Original longest palindromic substring in linear time.
"""

from __future__ import annotations


def longest_palindrome(s: str) -> str:
    if not s:
        return ""
    t = "#" + "#".join(s) + "#"
    n = len(t)
    p = [0] * n
    center = right = 0
    for i in range(n):
        mirror = 2 * center - i
        if i < right:
            p[i] = min(right - i, p[mirror])
        a = i + p[i] + 1
        b = i - p[i] - 1
        while a < n and b >= 0 and t[a] == t[b]:
            p[i] += 1
            a += 1
            b -= 1
        if i + p[i] > right:
            center = i
            right = i + p[i]
    max_len = max(p)
    idx = p.index(max_len)
    start = (idx - max_len) // 2
    return s[start:start + max_len]


if __name__ == "__main__":
    assert longest_palindrome("babad") in ("bab", "aba")
    assert longest_palindrome("cbbd") == "bb"
    assert longest_palindrome("a") == "a"
    print("manacher self-test passed")
