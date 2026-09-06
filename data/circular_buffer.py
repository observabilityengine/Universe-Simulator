"""Fixed-capacity circular (ring) buffer.

Complexity: O(1) push/pop.
Overwrites oldest when full if configured. Original implementation.
"""
from __future__ import annotations

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class CircularBuffer(Generic[T]):
    def __init__(self, capacity: int, overwrite: bool = True) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self.overwrite = overwrite
        self._buf: List[Optional[T]] = [None] * capacity
        self._head = 0  # next write
        self._tail = 0  # next read
        self._size = 0

    def push(self, item: T) -> bool:
        """Insert item. Returns False if full and overwrite=False."""
        if self._size == self.capacity:
            if not self.overwrite:
                return False
            self._tail = (self._tail + 1) % self.capacity
            self._size -= 1
        self._buf[self._head] = item
        self._head = (self._head + 1) % self.capacity
        self._size += 1
        return True

    def pop(self) -> T:
        if self._size == 0:
            raise IndexError("empty buffer")
        item = self._buf[self._tail]
        self._buf[self._tail] = None
        self._tail = (self._tail + 1) % self.capacity
        self._size -= 1
        return item  # type: ignore

    def __len__(self) -> int:
        return self._size

    def is_full(self) -> bool:
        return self._size == self.capacity


if __name__ == "__main__":
    buf = CircularBuffer[int](3)
    assert buf.push(1) and buf.push(2) and buf.push(3)
    assert buf.is_full()
    assert buf.push(4)  # overwrites 1
    assert buf.pop() == 2
    assert buf.pop() == 3
    assert buf.pop() == 4
    try:
        buf.pop()
        assert False
    except IndexError:
        pass
    buf2 = CircularBuffer[int](2, overwrite=False)
    assert buf2.push(1) and buf2.push(2)
    assert not buf2.push(3)
    print("circular_buffer self-tests passed")
