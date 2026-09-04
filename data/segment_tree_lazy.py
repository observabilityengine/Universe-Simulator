"""
Universe Simulator - Segment Tree with Lazy Propagation
Original range add + range sum.
"""

from __future__ import annotations

from typing import List

class LazySegmentTree:
    def __init__(self, data: List[float]):
        self.n = len(data)
        self.tree = [0.0] * (4 * self.n)
        self.lazy = [0.0] * (4 * self.n)
        if self.n:
            self._build(1, 0, self.n - 1, data)

    def _build(self, node: int, start: int, end: int, data: List[float]) -> None:
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        self._build(2*node, start, mid, data)
        self._build(2*node+1, mid+1, end, data)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def _push(self, node: int, start: int, end: int) -> None:
        if self.lazy[node] != 0:
            self.tree[node] += (end - start + 1) * self.lazy[node]
            if start != end:
                self.lazy[2*node] += self.lazy[node]
                self.lazy[2*node+1] += self.lazy[node]
            self.lazy[node] = 0.0

    def range_add(self, left: int, right: int, val: float) -> None:
        self._range_add(1, 0, self.n-1, left, right, val)

    def _range_add(self, node: int, start: int, end: int, left: int, right: int, val: float) -> None:
        self._push(node, start, end)
        if right < start or end < left:
            return
        if left <= start and end <= right:
            self.lazy[node] += val
            self._push(node, start, end)
            return
        mid = (start + end) // 2
        self._range_add(2*node, start, mid, left, right, val)
        self._range_add(2*node+1, mid+1, end, left, right, val)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def range_sum(self, left: int, right: int) -> float:
        return self._range_sum(1, 0, self.n-1, left, right)

    def _range_sum(self, node: int, start: int, end: int, left: int, right: int) -> float:
        self._push(node, start, end)
        if right < start or end < left:
            return 0.0
        if left <= start and end <= right:
            return self.tree[node]
        mid = (start + end) // 2
        return self._range_sum(2*node, start, mid, left, right) + self._range_sum(2*node+1, mid+1, end, left, right)

if __name__ == "__main__":
    st = LazySegmentTree([1.0, 2.0, 3.0, 4.0, 5.0])
    st.range_add(1, 3, 10.0)
    assert abs(st.range_sum(1, 3) - 39.0) < 1e-9
    print("segment_tree_lazy self-test passed")
