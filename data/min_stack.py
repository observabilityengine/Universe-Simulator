"""Stack supporting O(1) push, pop, top, and get_min.

Complexity: O(1) all operations; O(n) space.
Original implementation with parallel min stack.
"""
from __future__ import annotations

from typing import Generic, List, TypeVar

T = TypeVar("T")


class MinStack(Generic[T]):
    def __init__(self) -> None:
        self._data: List[T] = []
        self._mins: List[T] = []

    def push(self, val: T) -> None:
        self._data.append(val)
        if not self._mins or val <= self._mins[-1]:
            self._mins.append(val)

    def pop(self) -> T:
        if not self._data:
            raise IndexError("empty stack")
        val = self._data.pop()
        if val == self._mins[-1]:
            self._mins.pop()
        return val

    def top(self) -> T:
        if not self._data:
            raise IndexError("empty stack")
        return self._data[-1]

    def get_min(self) -> T:
        if not self._mins:
            raise IndexError("empty stack")
        return self._mins[-1]

    def __len__(self) -> int:
        return len(self._data)


if __name__ == "__main__":
    s = MinStack[int]()
    s.push(3)
    s.push(1)
    s.push(2)
    assert s.get_min() == 1
    assert s.pop() == 2
    assert s.get_min() == 1
    assert s.pop() == 1
    assert s.get_min() == 3
    assert s.top() == 3
    print("min_stack self-tests passed")
