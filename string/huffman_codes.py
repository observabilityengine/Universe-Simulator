"""Build optimal prefix codes from symbol frequencies (Huffman tree).

Complexity: O(n log n) for n symbols.
Returns mapping symbol → bitstring. Original implementation.
"""
from __future__ import annotations

import heapq
from typing import Dict, Hashable, List, Optional, Tuple


def huffman_codes(freq: Dict[Hashable, int]) -> Dict[Hashable, str]:
    """Return optimal prefix code table for given frequencies."""
    if not freq:
        return {}
    if len(freq) == 1:
        sym = next(iter(freq))
        return {sym: "0"}
    # heap entries: (freq, tie_id, symbol_or_None, left, right)
    heap: List[Tuple[int, int, Optional[Hashable], Optional[tuple], Optional[tuple]]] = []
    tie = 0
    for sym, f in freq.items():
        if f < 0:
            raise ValueError("frequencies must be non-negative")
        heapq.heappush(heap, (f, tie, sym, None, None))
        tie += 1
    while len(heap) > 1:
        f1, _, s1, l1, r1 = heapq.heappop(heap)
        f2, _, s2, l2, r2 = heapq.heappop(heap)
        node = (None, (f1, s1, l1, r1), (f2, s2, l2, r2))
        heapq.heappush(heap, (f1 + f2, tie, None, node[1], node[2]))
        tie += 1
    _, _, _, left, right = heap[0]
    codes: Dict[Hashable, str] = {}

    def walk(node: Optional[tuple], prefix: str) -> None:
        if node is None:
            return
        f, sym, l, r = node if len(node) == 4 else (node[0], node[1], None, None)
        # normalize
        if len(node) == 4:
            f, sym, l, r = node  # type: ignore
            if sym is not None:
                codes[sym] = prefix or "0"
                return
            walk(l, prefix + "0")
            walk(r, prefix + "1")

    # rebuild walk from heap root structure
    root_f, _, root_sym, root_l, root_r = heap[0]
    if root_sym is not None:
        codes[root_sym] = "0"
    else:
        def walk2(l, r, prefix: str) -> None:
            for bit, child in (("0", l), ("1", r)):
                if child is None:
                    continue
                f, s, cl, cr = child if len(child) == 4 else (*child, None, None)
                if len(child) == 4:
                    f, s, cl, cr = child
                if s is not None:
                    codes[s] = prefix + bit
                else:
                    walk2(cl, cr, prefix + bit)
        walk2(root_l, root_r, "")
    return codes


if __name__ == "__main__":
    codes = huffman_codes({"a": 5, "b": 2, "c": 1, "d": 1})
    assert set(codes.keys()) == {"a", "b", "c", "d"}
    # prefix-free: no code is prefix of another
    vals = list(codes.values())
    for i, c1 in enumerate(vals):
        for c2 in vals[i + 1 :]:
            assert not c1.startswith(c2) and not c2.startswith(c1)
    assert huffman_codes({}) == {}
    assert huffman_codes({"x": 1}) == {"x": "0"}
    print("huffman_codes self-tests passed")
