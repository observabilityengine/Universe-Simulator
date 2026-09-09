"""Write-Ahead Log for durability."""
from __future__ import annotations
from typing import Any, Dict, List


class WAL:
    def __init__(self):
        self.log: List[Dict[str, Any]] = []
        self.flushed = 0

    def append(self, op: str, key: Any, value: Any = None) -> int:
        entry = {"lsn": len(self.log), "op": op, "key": key, "value": value}
        self.log.append(entry)
        return entry["lsn"]

    def flush(self) -> None:
        self.flushed = len(self.log)

    def replay(self) -> List[Dict[str, Any]]:
        return self.log[: self.flushed]

    def truncate(self, lsn: int) -> None:
        self.log = self.log[lsn:]
        self.flushed = max(0, self.flushed - lsn)


if __name__ == "__main__":
    wal = WAL()
    wal.append("PUT", "x", 1)
    wal.append("PUT", "y", 2)
    wal.flush()
    wal.append("DELETE", "x")
    assert len(wal.replay()) == 2
    print(f"wal flushed={wal.flushed}")
    print("wal self-tests passed")
