"""Boyer-Moore string search (bad-character heuristic)."""
from __future__ import annotations
from typing import Dict, List


def _bad_char_table(pattern: str) -> Dict[str, int]:
    table = {}
    for i, ch in enumerate(pattern):
        table[ch] = i
    return table


def boyer_moore_search(text: str, pattern: str) -> List[int]:
    if not pattern:
        return list(range(len(text) + 1))
    if len(pattern) > len(text):
        return []
    bad = _bad_char_table(pattern)
    m, n = len(pattern), len(text)
    matches = []
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            matches.append(i)
            i += 1
        else:
            bc = bad.get(text[i + j], -1)
            i += max(1, j - bc)
    return matches


if __name__ == "__main__":
    assert boyer_moore_search("ababcabcabababd", "ababd") == [10]
    assert boyer_moore_search("aaaa", "aa") == [0, 1, 2]
    assert boyer_moore_search("hello", "x") == []
    print("boyer_moore self-tests passed")
