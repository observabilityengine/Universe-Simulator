"""Boyer-Moore-Horspool string search (simplified Boyer-Moore).

Complexity: average O(n/m) for pattern length m, text length n; worst O(n*m).
Returns starting indices of all non-overlapping occurrences.
Original implementation.
"""
from __future__ import annotations

from typing import List


def boyer_moore(text: str, pattern: str) -> List[int]:
    """Return list of start indices where pattern occurs in text."""
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    # bad-character shift table
    shift = {c: m for c in set(text)}
    for i in range(m - 1):
        shift[pattern[i]] = m - 1 - i
    result: List[int] = []
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            result.append(i)
            i += m  # non-overlapping
        else:
            i += shift.get(text[i + m - 1], m)
    return result


if __name__ == "__main__":
    assert boyer_moore("abracadabra", "abra") == [0, 7]
    assert boyer_moore("aaaa", "aa") == [0, 2]
    assert boyer_moore("hello", "xyz") == []
    assert boyer_moore("", "a") == []
    assert boyer_moore("abc", "") == [0, 1, 2, 3]
    assert boyer_moore("abc", "abc") == [0]
    assert boyer_moore("a", "a") == [0]
    print("boyer_moore self-tests passed")
