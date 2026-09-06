"""LZ78 dictionary compression.

Complexity: O(n) encode/decode for input length n.
Returns list of (index, char) phrases; index 0 means empty prefix.
Original implementation.
"""
from __future__ import annotations

from typing import List, Tuple


def lz78_encode(data: bytes) -> List[Tuple[int, int]]:
    """Encode bytes to list of (dict_index, next_byte)."""
    if not data:
        return []
    dictionary = {b"": 0}
    phrases: List[Tuple[int, int]] = []
    w = b""
    next_idx = 1
    for b in data:
        wb = w + bytes([b])
        if wb in dictionary:
            w = wb
        else:
            phrases.append((dictionary[w], b))
            dictionary[wb] = next_idx
            next_idx += 1
            w = b""
    if w:
        # final phrase without new char — emit index only with char 0 sentinel unused
        # standard: last phrase is (index of w, empty) — we use char=-1 marker avoided;
        # emit each remaining as extension of known
        phrases.append((dictionary[w[:-1]] if len(w) > 1 else 0, w[-1]))
    return phrases


def lz78_decode(phrases: List[Tuple[int, int]]) -> bytes:
    """Decode phrase list back to bytes."""
    dictionary = {0: b""}
    out = bytearray()
    next_idx = 1
    for idx, byte in phrases:
        entry = dictionary[idx] + bytes([byte])
        out.extend(entry)
        dictionary[next_idx] = entry
        next_idx += 1
    return bytes(out)


if __name__ == "__main__":
    original = b"ABABABA"
    enc = lz78_encode(original)
    dec = lz78_decode(enc)
    assert dec == original
    assert lz78_decode(lz78_encode(b"")) == b""
    assert lz78_decode(lz78_encode(b"X")) == b"X"
    s = b"TOBEORNOTTOBEORTOBEORNOT"
    assert lz78_decode(lz78_encode(s)) == s
    print("lz78 self-tests passed")
