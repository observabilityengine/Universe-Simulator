"""Run-length encoding / decoding for strings."""
from __future__ import annotations


def rle_encode(s: str) -> str:
    if not s:
        return ""
    out = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            out.append(f"{count}{s[i - 1]}")
            count = 1
    out.append(f"{count}{s[-1]}")
    return "".join(out)


def rle_decode(encoded: str) -> str:
    out = []
    i = 0
    while i < len(encoded):
        j = i
        while j < len(encoded) and encoded[j].isdigit():
            j += 1
        count = int(encoded[i:j]) if j > i else 1
        if j < len(encoded):
            out.append(encoded[j] * count)
            i = j + 1
        else:
            break
    return "".join(out)


if __name__ == "__main__":
    e = rle_encode("aaabbbcc")
    assert rle_decode(e) == "aaabbbcc"
    print(f"run_length_string {e}")
    print("run_length_string self-tests passed")
