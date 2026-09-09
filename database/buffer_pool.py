"""Buffer pool with LRU page replacement."""
from __future__ import annotations
from collections import OrderedDict
from typing import Any, Optional


class BufferPool:
    def __init__(self, capacity: int = 32):
        self.capacity = capacity
        self.pages: OrderedDict[int, Any] = OrderedDict()
        self.dirty: set = set()

    def get(self, page_id: int, loader=None) -> Any:
        if page_id in self.pages:
            self.pages.move_to_end(page_id)
            return self.pages[page_id]
        if loader is None:
            return None
        data = loader(page_id)
        self.put(page_id, data)
        return data

    def put(self, page_id: int, data: Any, dirty: bool = False) -> None:
        if page_id in self.pages:
            self.pages.move_to_end(page_id)
            self.pages[page_id] = data
        else:
            if len(self.pages) >= self.capacity:
                evicted, _ = self.pages.popitem(last=False)
                self.dirty.discard(evicted)
            self.pages[page_id] = data
        if dirty:
            self.dirty.add(page_id)

    def flush(self, writer) -> int:
        count = 0
        for pid in list(self.dirty):
            writer(pid, self.pages[pid])
            self.dirty.discard(pid)
            count += 1
        return count


if __name__ == "__main__":
    bp = BufferPool(capacity=2)
    bp.put(1, "a")
    bp.put(2, "b")
    bp.put(3, "c")
    assert bp.get(1) is None
    assert bp.get(2) == "b"
    print("buffer_pool self-tests passed")
