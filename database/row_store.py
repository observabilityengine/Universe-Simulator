"""Row-oriented heap file store."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


class RowStore:
    def __init__(self):
        self.rows: List[Dict[str, Any]] = []
        self.free: List[int] = []

    def insert(self, row: Dict[str, Any]) -> int:
        if self.free:
            rid = self.free.pop()
            self.rows[rid] = row
            return rid
        self.rows.append(row)
        return len(self.rows) - 1

    def get(self, rid: int) -> Optional[Dict[str, Any]]:
        if 0 <= rid < len(self.rows) and self.rows[rid] is not None:
            return self.rows[rid]
        return None

    def delete(self, rid: int) -> bool:
        if 0 <= rid < len(self.rows) and self.rows[rid] is not None:
            self.rows[rid] = None
            self.free.append(rid)
            return True
        return False

    def scan(self) -> List[Dict[str, Any]]:
        return [r for r in self.rows if r is not None]


if __name__ == "__main__":
    rs = RowStore()
    r0 = rs.insert({"a": 1})
    r1 = rs.insert({"a": 2})
    assert rs.get(r0)["a"] == 1
    rs.delete(r0)
    assert rs.get(r0) is None
    assert len(rs.scan()) == 1
    print("row_store self-tests passed")
