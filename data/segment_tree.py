"""
Universe Simulator - Segment Tree (range sum / point update)
Original pure-Python implementation.
"""

from __future__ import annotations

from typing import List


class SegmentTree:
    def __init__(self, data: List[float]):
        self.n = len(data)
        self.tree = [0.0] * (4 * self.n + 4)
        if self.n:
            self._build(1, 0, self.n - 1, data)

    def _build(self, node: int, start: int, end: int, data: List[float]) -> None:
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        self._build(2 * node, start, mid, data)
        self._build(2 * node + 1, mid + 1, end, data)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, idx: int, value: float) -> None:
        self._update(1, 0, self.n - 1, idx, value)

    def _update(self, node: int, start: int, end: int, idx: int, value: float) -> None:
        if start == end:
            self.tree[node] = value
            return
        mid = (start + end) // 2
        if idx <= mid:
            self._update(2 * node, start, mid, idx, value)
        else:
            self._update(2 * node + 1, mid + 1, end, idx, value)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, left: int, right: int) -> float:
        return self._query(1, 0, self.n - 1, left, right)

    def _query(self, node: int, start: int, end: int, left: int, right: int) -> float:
        if right < start or end < left:
            return 0.0
        if left <= start and end <= right:
            return self.tree[node]
        mid = (start + end) // 2
        return self._query(2 * node, start, mid, left, right) + self._query(2 * node + 1, mid + 1, end, left, right)


if __name__ == "__main__":
    st = SegmentTree([1.0, 3.0, 5.0, 7.0, 9.0, 11.0])
    assert abs(st.query(1, 3) - 15.0) < 1e-9
    st.update(2, 10.0)
    assert abs(st.query(1, 3) - 20.0) < 1e-9
    print("segment_tree self-test passed")
