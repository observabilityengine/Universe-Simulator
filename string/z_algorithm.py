"""Z-algorithm for string matching / prefix analysis.

Complexity: O(n). Original implementation.
"""
from __future__ import annotations

from typing import List


def z_array(s: str) -> List[int]:
    """Z[i] = length of longest substring starting at i that matches prefix of s."""
    n = len(s)
    z = [0] * n
    z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def z_search(text: str, pattern: str) -> List[int]:
    """Find all occurrences of pattern in text using Z-algorithm."""
    concat = pattern + "$" + text
    z = z_array(concat)
    m = len(pattern)
    return [i - m - 1 for i in range(m + 1, len(concat)) if z[i] == m]


if __name__ == "__main__":
    z = z_array("aabcaabxaaaz")
    assert z[0] == 12
    assert z[4] == 3
    assert z_search("ababcabcabababd", "ababd") == [10]
    assert z_search("aaaa", "aa") == [0, 1, 2]
    print("z_algorithm self-tests passed")
