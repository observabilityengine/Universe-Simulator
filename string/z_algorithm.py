"""
Universe Simulator - Z-Algorithm
Original linear-time string matching via Z-array.
"""

from __future__ import annotations

from typing import List


def z_array(s: str) -> List[int]:
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z


def z_search(text: str, pattern: str) -> List[int]:
    if not pattern:
        return []
    concat = pattern + "$" + text
    z = z_array(concat)
    m = len(pattern)
    return [i - m - 1 for i in range(m + 1, len(concat)) if z[i] == m]


if __name__ == "__main__":
    assert z_search("abxabcabcaby", "abcaby") == [6]
    assert z_search("aaaaa", "aa") == [0, 1, 2, 3]
    print("z_algorithm self-test passed")
