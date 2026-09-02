"""
Module 36 – LRU Cache
O(1) Least-Recently-Used cache.
Original implementation.
"""

from __future__ import annotations
from typing import Any, Optional
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self._data: OrderedDict[Any, Any] = OrderedDict()

    def get(self, key: Any) -> Optional[Any]:
        if key not in self._data:
            return None
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key: Any, value: Any) -> None:
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def __contains__(self, key: Any) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def keys(self):
        return list(self._data.keys())


if __name__ == "__main__":
    print("Testing LRU Cache...")
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    print(f"  Get a: {cache.get('a')}")
    cache.put("d", 4)
    print(f"  Contains b: {'b' in cache}")
    print(f"  Keys: {cache.keys()}")
    print("LRU Cache module OK.")
