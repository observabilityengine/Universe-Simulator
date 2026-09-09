"""Page cache with pin/unpin and clock replacement."""
from __future__ import annotations
from typing import Any, Dict


class PageCache:
    def __init__(self, capacity: int = 32):
        self.capacity = capacity
        self.pages: Dict[int, Any] = {}
        self.ref: Dict[int, bool] = {}
        self.pin_count: Dict[int, int] = {}
        self.clock_hand = 0
        self.page_ids: list = []

    def pin(self, page_id: int, data: Any = None) -> Any:
        if page_id in self.pages:
            self.pin_count[page_id] = self.pin_count.get(page_id, 0) + 1
            self.ref[page_id] = True
            return self.pages[page_id]
        if len(self.pages) >= self.capacity:
            self._evict()
        self.pages[page_id] = data
        self.pin_count[page_id] = 1
        self.ref[page_id] = True
        self.page_ids.append(page_id)
        return data

    def unpin(self, page_id: int) -> None:
        if page_id in self.pin_count and self.pin_count[page_id] > 0:
            self.pin_count[page_id] -= 1

    def _evict(self) -> None:
        n = len(self.page_ids)
        if n == 0:
            return
        for _ in range(n * 2):
            pid = self.page_ids[self.clock_hand % n]
            self.clock_hand += 1
            if self.pin_count.get(pid, 0) > 0:
                continue
            if self.ref.get(pid):
                self.ref[pid] = False
                continue
            del self.pages[pid]
            del self.ref[pid]
            del self.pin_count[pid]
            self.page_ids.remove(pid)
            return


if __name__ == "__main__":
    pc = PageCache(capacity=2)
    pc.pin(1, "A")
    pc.pin(2, "B")
    pc.unpin(1)
    pc.pin(3, "C")
    assert 1 not in pc.pages
    print("page_cache self-tests passed")
