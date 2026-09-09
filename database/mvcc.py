"""Multi-Version Concurrency Control – snapshot isolation."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple


class Version:
    def __init__(self, value: Any, begin_ts: int, end_ts: int = float("inf")):
        self.value = value
        self.begin_ts = begin_ts
        self.end_ts = end_ts


class MVCCStore:
    def __init__(self):
        self.data: Dict[str, List[Version]] = {}
        self.ts = 0

    def begin(self) -> int:
        self.ts += 1
        return self.ts

    def read(self, key: str, ts: int) -> Optional[Any]:
        versions = self.data.get(key, [])
        for v in reversed(versions):
            if v.begin_ts <= ts < v.end_ts:
                return v.value
        return None

    def write(self, key: str, value: Any, ts: int) -> None:
        versions = self.data.setdefault(key, [])
        for v in versions:
            if v.end_ts == float("inf"):
                v.end_ts = ts
        versions.append(Version(value, ts))


if __name__ == "__main__":
    store = MVCCStore()
    t1 = store.begin()
    store.write("x", 10, t1)
    t2 = store.begin()
    assert store.read("x", t2) == 10
    store.write("x", 20, t2)
    assert store.read("x", t1) == 10
    assert store.read("x", t2) == 20
    print("mvcc self-tests passed")
