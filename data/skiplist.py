"""
Module 39 – Skip List
Probabilistic ordered map with O(log n) operations.
Original implementation.
"""

from __future__ import annotations
import random
from typing import Any, Optional, List


class _Node:
    __slots__ = ("key", "value", "forward")
    def __init__(self, key: Any, value: Any, level: int):
        self.key = key
        self.value = value
        self.forward: List[Optional[_Node]] = [None] * (level + 1)


class SkipList:
    def __init__(self, max_level: int = 16, p: float = 0.5):
        self.max_level = max_level
        self.p = p
        self.level = 0
        self.header = _Node(None, None, max_level)
        self._size = 0

    def _random_level(self) -> int:
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, key: Any, value: Any) -> None:
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]
        if current and current.key == key:
            current.value = value
            return
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.header
            self.level = lvl
        new_node = _Node(key, value, lvl)
        for i in range(lvl + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node
        self._size += 1

    def search(self, key: Any) -> Optional[Any]:
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.key == key:
            return current.value
        return None

    def __len__(self) -> int:
        return self._size


if __name__ == "__main__":
    print("Testing Skip List...")
    sl = SkipList()
    for k, v in [(5, "e"), (1, "a"), (3, "c"), (2, "b"), (4, "d")]:
        sl.insert(k, v)
    print(f"  search(3) = {sl.search(3)}")
    print(f"  size = {len(sl)}")
    print("Skip List module OK.")
