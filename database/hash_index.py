"""Hash index with chaining."""
from __future__ import annotations
from typing import Any, List, Optional, Tuple


class HashIndex:
    def __init__(self, buckets: int = 16):
        self.buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(buckets)]
        self.n = buckets

    def _idx(self, key: Any) -> int:
        return hash(key) % self.n

    def put(self, key: Any, value: Any) -> None:
        b = self.buckets[self._idx(key)]
        for i, (k, _) in enumerate(b):
            if k == key:
                b[i] = (key, value)
                return
        b.append((key, value))

    def get(self, key: Any) -> Optional[Any]:
        for k, v in self.buckets[self._idx(key)]:
            if k == key:
                return v
        return None

    def delete(self, key: Any) -> bool:
        b = self.buckets[self._idx(key)]
        for i, (k, _) in enumerate(b):
            if k == key:
                b.pop(i)
                return True
        return False


if __name__ == "__main__":
    h = HashIndex()
    h.put("a", 1)
    h.put("b", 2)
    assert h.get("a") == 1
    assert h.delete("a")
    assert h.get("a") is None
    print("hash_index self-tests passed")
