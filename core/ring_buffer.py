"""
Universe Simulator - Fixed-size Ring Buffer
Original circular buffer for streaming data.
"""

from __future__ import annotations

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class RingBuffer(Generic[T]):
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self.buf: List[Optional[T]] = [None] * capacity
        self.head = 0
        self.tail = 0
        self.size = 0

    def push(self, item: T) -> None:
        self.buf[self.tail] = item
        self.tail = (self.tail + 1) % self.capacity
        if self.size < self.capacity:
            self.size += 1
        else:
            self.head = (self.head + 1) % self.capacity

    def pop(self) -> T:
        if self.size == 0:
            raise IndexError("empty ring buffer")
        item = self.buf[self.head]
        self.buf[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return item  # type: ignore

    def __len__(self) -> int:
        return self.size


if __name__ == "__main__":
    rb = RingBuffer[int](3)
    rb.push(1)
    rb.push(2)
    rb.push(3)
    rb.push(4)  # overwrites 1
    assert len(rb) == 3
    assert rb.pop() == 2
    assert rb.pop() == 3
    assert rb.pop() == 4
    print("ring_buffer self-test passed")
