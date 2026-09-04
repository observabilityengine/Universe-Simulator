"""
Universe Simulator - Skip List Map
Original probabilistic balanced map with insert / search / delete.
"""

from __future__ import annotations

import random
from typing import Any, List, Optional

class SLNode:
    def __init__(self, key: Any, value: Any, level: int):
        self.key = key
        self.value = value
        self.forward: List[Optional["SLNode"]] = [None] * (level + 1)

class SkipListMap:
    def __init__(self, max_level: int = 16, p: float = 0.5, seed: int = 42):
        self.max_level = max_level
        self.p = p
        self.rng = random.Random(seed)
        self.header = SLNode(None, None, max_level)
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
        update = [None] * (self.max_level + 1)
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
        node = SLNode(key, value, lvl)
        for i in range(lvl + 1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

if __name__ == "__main__":
    sl = SkipListMap()
    sl.insert(5, "a")
    sl.insert(3, "b")
    sl.insert(7, "c")
    assert sl.search(5) == "a" and sl.search(3) == "b" and sl.search(1) is None
    print("skip_list_map self-test passed")
