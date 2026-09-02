"""
Module 76 – LFU Cache
Least-Frequently-Used cache with O(1) operations.
Complete implementation.
"""

from __future__ import annotations
from collections import defaultdict, OrderedDict
from typing import Any, Optional


class LFUCache:
    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        self.capacity = capacity
        self._val: dict = {}
        self._freq: dict = {}
        self._freq_to_keys: dict = defaultdict(OrderedDict)
        self._min_freq = 0

    def _update_freq(self, key: Any) -> None:
        freq = self._freq[key]
        del self._freq_to_keys[freq][key]
        if not self._freq_to_keys[freq] and freq == self._min_freq:
            self._min_freq += 1
        self._freq[key] = freq + 1
        self._freq_to_keys[freq + 1][key] = None

    def get(self, key: Any) -> Optional[Any]:
        if key not in self._val:
            return None
        self._update_freq(key)
        return self._val[key]

    def put(self, key: Any, value: Any) -> None:
        if self.capacity == 0:
            return
        if key in self._val:
            self._val[key] = value
            self._update_freq(key)
            return
        if len(self._val) >= self.capacity:
            evict_key, _ = self._freq_to_keys[self._min_freq].popitem(last=False)
            del self._val[evict_key]
            del self._freq[evict_key]
        self._val[key] = value
        self._freq[key] = 1
        self._freq_to_keys[1][key] = None
        self._min_freq = 1

    def __len__(self) -> int:
        return len(self._val)

    def __contains__(self, key: Any) -> bool:
        return key in self._val


if __name__ == "__main__":
    print("Testing LFU Cache...")
    cache = LFUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    print(f"  get a: {cache.get('a')}")
    cache.put("c", 3)
    print(f"  contains b: {'b' in cache}")
    print(f"  get c: {cache.get('c')}")
    print(f"  size: {len(cache)}")
    print("LFU Cache module OK.")
