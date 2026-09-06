"""Binary max-heap.

Complexity: O(log n) push/pop; O(n) heapify.
Original implementation.
"""
from __future__ import annotations

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class MaxHeap(Generic[T]):
    def __init__(self, data: Optional[List[T]] = None) -> None:
        self._a: List[T] = list(data) if data else []
        if self._a:
            self._heapify()

    def _sift_up(self, i: int) -> None:
        while i > 0:
            p = (i - 1) // 2
            if self._a[i] <= self._a[p]:
                break
            self._a[i], self._a[p] = self._a[p], self._a[i]
            i = p

    def _sift_down(self, i: int) -> None:
        n = len(self._a)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            largest = i
            if left < n and self._a[left] > self._a[largest]:
                largest = left
            if right < n and self._a[right] > self._a[largest]:
                largest = right
            if largest == i:
                break
            self._a[i], self._a[largest] = self._a[largest], self._a[i]
            i = largest

    def _heapify(self) -> None:
        for i in range(len(self._a) // 2 - 1, -1, -1):
            self._sift_down(i)

    def push(self, val: T) -> None:
        self._a.append(val)
        self._sift_up(len(self._a) - 1)

    def pop(self) -> T:
        if not self._a:
            raise IndexError("empty heap")
        self._a[0], self._a[-1] = self._a[-1], self._a[0]
        val = self._a.pop()
        if self._a:
            self._sift_down(0)
        return val

    def peek(self) -> T:
        if not self._a:
            raise IndexError("empty heap")
        return self._a[0]

    def __len__(self) -> int:
        return len(self._a)


if __name__ == "__main__":
    h = MaxHeap([3, 1, 4, 1, 5])
    assert h.peek() == 5
    assert h.pop() == 5
    h.push(9)
    assert h.pop() == 9
    out = []
    while h:
        out.append(h.pop())
    assert out == sorted(out, reverse=True)
    print("max_heap self-tests passed")
