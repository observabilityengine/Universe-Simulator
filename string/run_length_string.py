"""Run-length encoding for Unicode strings.

Complexity: O(n).
Encodes as list of (char, count). Original implementation.
"""
from __future__ import annotations

from typing import List, Tuple


def rle_string_encode(s: str) -> List[Tuple[str, int]]:
    if not s:
        return []
    out: List[Tuple[str, int]] = []
    prev = s[0]
    count = 1
    for ch in s[1:]:
        if ch == prev:
            count += 1
        else:
            out.append((prev, count))
            prev = ch
            count = 1
    out.append((prev, count))
    return out


def rle_string_decode(encoded: List[Tuple[str, int]]) -> str:
    parts: List[str] = []
    for ch, cnt in encoded:
        if cnt < 1 or len(ch) != 1:
            raise ValueError("invalid RLE pair")
        parts.append(ch * cnt)
    return "".join(parts)


if __name__ == "__main__":
    s = "aaabbbccdaa"
    enc = rle_string_encode(s)
    assert rle_string_decode(enc) == s
    assert rle_string_encode("") == []
    assert rle_string_decode([]) == ""
    assert rle_string_decode(rle_string_encode("xyz")) == "xyz"
    assert rle_string_encode("aaaa") == [("a", 4)]
    print("run_length_string self-tests passed")
