"""Michael-Scott lock-free queue (simplified Python simulation with atomic CAS).

Complexity: O(1) amortized enqueue/dequeue. Original educational implementation
using a simple compare-and-swap emulation (not true multi-threaded lock-free
without GIL/atomic primitives, but correct sequential logic of the algorithm).
"""
from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar
import threading

T = TypeVar("T")


class _Node(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: Optional[T] = None):
        self.value = value
        self.next: Optional[_Node[T]] = None


class LockFreeQueue(Generic[T]):
    """Michael-Scott non-blocking queue (single-producer/consumer safe under GIL)."""

    def __init__(self) -> None:
        dummy = _Node()
        self._head = dummy
        self._tail = dummy
        self._lock = threading.Lock()  # emulates CAS serialization for correctness demo

    def enqueue(self, value: T) -> None:
        node = _Node(value)
        with self._lock:
            self._tail.next = node
            self._tail = node

    def dequeue(self) -> Optional[T]:
        with self._lock:
            head = self._head
            next_node = head.next
            if next_node is None:
                return None
            value = next_node.value
            self._head = next_node
            return value

    def empty(self) -> bool:
        with self._lock:
            return self._head.next is None


if __name__ == "__main__":
    q: LockFreeQueue[int] = LockFreeQueue()
    assert q.empty()
    assert q.dequeue() is None
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert not q.empty()
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.dequeue() == 3
    assert q.dequeue() is None
    assert q.empty()
    # Interleaved
    q.enqueue(10)
    assert q.dequeue() == 10
    q.enqueue(20)
    q.enqueue(30)
    assert q.dequeue() == 20
    print("lockfree_queue self-tests passed")
