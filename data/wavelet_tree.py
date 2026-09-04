"""
Universe Simulator - Wavelet Tree
Original rank/select structure for sequences.
"""

from __future__ import annotations

from typing import List, Optional

class WaveletNode:
    def __init__(self, lo: int, hi: int):
        self.lo = lo
        self.hi = hi
        self.bit: List[int] = []
        self.left: Optional["WaveletNode"] = None
        self.right: Optional["WaveletNode"] = None

class WaveletTree:
    def __init__(self, seq: List[int], alphabet_max: int):
        self.root = self._build(seq, 0, alphabet_max)

    def _build(self, seq: List[int], lo: int, hi: int) -> Optional[WaveletNode]:
        if not seq or lo > hi:
            return None
        node = WaveletNode(lo, hi)
        if lo == hi:
            return node
        mid = (lo + hi) // 2
        left_seq, right_seq = [], []
        for x in seq:
            if x <= mid:
                node.bit.append(0)
                left_seq.append(x)
            else:
                node.bit.append(1)
                right_seq.append(x)
        node.left = self._build(left_seq, lo, mid)
        node.right = self._build(right_seq, mid + 1, hi)
        return node

    def rank(self, pos: int, value: int) -> int:
        return self._rank(self.root, pos, value)

    def _rank(self, node: Optional[WaveletNode], pos: int, value: int) -> int:
        if not node or pos <= 0:
            return 0
        if node.lo == node.hi:
            return pos
        mid = (node.lo + node.hi) // 2
        zeros = sum(1 for b in node.bit[:pos] if b == 0)
        if value <= mid:
            return self._rank(node.left, zeros, value)
        return self._rank(node.right, pos - zeros, value)

if __name__ == "__main__":
    seq = [3, 1, 4, 1, 5, 9, 2, 6]
    wt = WaveletTree(seq, 9)
    assert wt.rank(5, 1) == 2
    assert wt.rank(8, 1) == 2
    print("wavelet_tree self-test passed")
