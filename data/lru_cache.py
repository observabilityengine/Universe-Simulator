"""LRU Cache.

Complexity: O(1) get/put. Original implementation.
"""
from __future__ import annotations
from typing import Any, Optional, Dict

class _Node:
    __slots__ = ("key", "value", "prev", "next")
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.map: Dict[Any, _Node] = {}
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add(self, node: _Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: Any) -> Optional[Any]:
        if key not in self.map:
            return None
        node = self.map[key]
        self._remove(node)
        self._add(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        if key in self.map:
            self._remove(self.map[key])
        node = _Node(key, value)
        self._add(node)
        self.map[key] = node
        if len(self.map) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]

if __name__ == "__main__":
    c = LRUCache(2)
    c.put(1, 10)
    c.put(2, 20)
    assert c.get(1) == 10
    c.put(3, 30)
    assert c.get(2) is None
    assert c.get(3) == 30
    print("lru_cache self-tests passed")
