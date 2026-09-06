"""Double-ended queue on a dynamic circular buffer.

Complexity: amortized O(1) append/pop left/right.
Original implementation.
"""
from __future__ import annotations

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class Deque(Generic[T]):
    def __init__(self, capacity: int = 8) -> None:
        self._buf: List[Optional[T]] = [None] * max(8, capacity)
        self._head = 0
        self._tail = 0
        self._size = 0

    def _grow(self) -> None:
        n = len(self._buf)
        new = [None] * (n * 2)
        for i in range(self._size):
            new[i] = self._buf[(self._head + i) % n]
        self._buf = new  # type: ignore
        self._head = 0
        self._tail = self._size

    def append(self, item: T) -> None:
        if self._size == len(self._buf):
            self._grow()
        self._buf[self._tail] = item
        self._tail = (self._tail + 1) % len(self._buf)
        self._size += 1

    def appendleft(self, item: T) -> None:
        if self._size == len(self._buf):
            self._grow()
        self._head = (self._head - 1) % len(self._buf)
        self._buf[self._head] = item
        self._size += 1

    def pop(self) -> T:
        if self._size == 0:
            raise IndexError("empty deque")
        self._tail = (self._tail - 1) % len(self._buf)
        item = self._buf[self._tail]
        self._buf[self._tail] = None
        self._size -= 1
        return item  # type: ignore

    def popleft(self) -> T:
        if self._size == 0:
            raise IndexError("empty deque")
        item = self._buf[self._head]
        self._buf[self._head] = None
        self._head = (self._head + 1) % len(self._buf)
        self._size -= 1
        return item  # type: ignore

    def __len__(self) -> int:
        return self._size


if __name__ == "__main__":
    d = Deque[int]()
    d.append(1)
    d.append(2)
    d.appendleft(0)
    assert d.popleft() == 0
    assert d.pop() == 2
    assert d.pop() == 1
    try:
        d.pop()
        assert False
    except IndexError:
        pass
    print("deque_ring self-tests passed")
