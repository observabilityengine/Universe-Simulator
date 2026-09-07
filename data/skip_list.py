"""Skip list (probabilistic ordered dictionary).

Complexity: O(log n) expected for search/insert/delete. Original implementation.
"""
from __future__ import annotations
import random
from typing import Any, Optional, List

class _Node:
    __slots__ = ("key", "value", "forward")
    def __init__(self, key: Any, value: Any, level: int) -> None:
        self.key = key
        self.value = value
        self.forward: List[Optional["_Node"]] = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level: int = 16, p: float = 0.5, seed: int = 42) -> None:
        self.max_level = max_level
        self.p = p
        self.rng = random.Random(seed)
        self.header = _Node(None, None, max_level)
        self.level = 0

    def _random_level(self) -> int:
        lvl = 0
        while self.rng.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def search(self, key: Any) -> Optional[Any]:
        cur = self.header
        for i in range(self.level, -1, -1):
            while cur.forward[i] and cur.forward[i].key < key:
                cur = cur.forward[i]
        cur = cur.forward[0]
        if cur and cur.key == key:
            return cur.value
        return None

    def insert(self, key: Any, value: Any) -> None:
        update: List[_Node] = [self.header] * (self.max_level + 1)
        cur = self.header
        for i in range(self.level, -1, -1):
            while cur.forward[i] and cur.forward[i].key < key:
                cur = cur.forward[i]
            update[i] = cur
        cur = cur.forward[0]
        if cur and cur.key == key:
            cur.value = value
            return
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.header
            self.level = lvl
        node = _Node(key, value, lvl)
        for i in range(lvl + 1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

    def delete(self, key: Any) -> bool:
        update: List[_Node] = [self.header] * (self.max_level + 1)
        cur = self.header
        for i in range(self.level, -1, -1):
            while cur.forward[i] and cur.forward[i].key < key:
                cur = cur.forward[i]
            update[i] = cur
        cur = cur.forward[0]
        if not cur or cur.key != key:
            return False
        for i in range(self.level + 1):
            if update[i].forward[i] != cur:
                break
            update[i].forward[i] = cur.forward[i]
        while self.level > 0 and self.header.forward[self.level] is None:
            self.level -= 1
        return True

if __name__ == "__main__":
    sl = SkipList(seed=1)
    for i in range(50):
        sl.insert(i, i * 10)
    assert sl.search(25) == 250
    assert sl.search(100) is None
    assert sl.delete(25)
    assert sl.search(25) is None
    print("skip_list self-tests passed")
