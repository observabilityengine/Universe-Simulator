"""
Module 50 – Interval Tree (simplified)
Store intervals and query point overlaps.
Original implementation using sorted list.
"""

from __future__ import annotations
from typing import List, Tuple, Any


class IntervalTree:
    def __init__(self):
        self._intervals: List[Tuple[float, float, Any]] = []

    def add(self, start: float, end: float, value: Any = None) -> None:
        if end < start:
            start, end = end, start
        self._intervals.append((start, end, value))
        self._intervals.sort(key=lambda x: x[0])

    def query_point(self, point: float) -> List[Any]:
        return [v for s, e, v in self._intervals if s <= point <= e]

    def query_range(self, start: float, end: float) -> List[Any]:
        if end < start:
            start, end = end, start
        return [v for s, e, v in self._intervals if not (e < start or s > end)]

    def __len__(self) -> int:
        return len(self._intervals)


if __name__ == "__main__":
    print("Testing Interval Tree...")
    it = IntervalTree()
    it.add(1, 5, "A")
    it.add(3, 8, "B")
    it.add(10, 15, "C")
    print(f"  Point 4: {it.query_point(4)}")
    print(f"  Point 9: {it.query_point(9)}")
    print(f"  Range 6-12: {it.query_range(6, 12)}")
    print("Interval Tree module OK.")
