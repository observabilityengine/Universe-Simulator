"""
Universe Simulator - Binary Heap Priority Queue
Original min-heap.
"""

from __future__ import annotations

from typing import Any, List, Tuple


class PriorityQueue:
    def __init__(self) -> None:
        self._heap: List[Tuple[float, int, Any]] = []
        self._count = 0

    def push(self, priority: float, item: Any) -> None:
        self._count += 1
        self._heap.append((priority, self._count, item))
        self._sift_up(len(self._heap) - 1)

    def pop(self) -> Any:
        if not self._heap:
            raise IndexError("empty")
        self._swap(0, len(self._heap) - 1)
        item = self._heap.pop()[2]
        if self._heap:
            self._sift_down(0)
        return item

    def _sift_up(self, i: int) -> None:
        while i > 0:
            p = (i - 1) // 2
            if self._heap[i] < self._heap[p]:
                self._swap(i, p)
                i = p
            else:
                break

    def _sift_down(self, i: int) -> None:
        n = len(self._heap)
        while True:
            left = 2 * i + 1
            right = left + 1
            smallest = i
            if left < n and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < n and self._heap[right] < self._heap[smallest]:
                smallest = right
            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest

    def _swap(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def __len__(self) -> int:
        return len(self._heap)


if __name__ == "__main__":
    pq = PriorityQueue()
    pq.push(3, "c")
    pq.push(1, "a")
    pq.push(2, "b")
    assert pq.pop() == "a" and pq.pop() == "b" and pq.pop() == "c"
    print("priority_queue self-test passed")
