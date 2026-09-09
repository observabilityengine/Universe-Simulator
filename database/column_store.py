"""Column-oriented store with dictionary encoding."""
from __future__ import annotations
from typing import Any, Dict, List


class Column:
    def __init__(self, name: str):
        self.name = name
        self.data: List[Any] = []
        self.dict_encode: Dict[Any, int] = {}
        self.dict_decode: List[Any] = []

    def append(self, value: Any) -> None:
        if value not in self.dict_encode:
            self.dict_encode[value] = len(self.dict_decode)
            self.dict_decode.append(value)
        self.data.append(self.dict_encode[value])

    def get(self, i: int) -> Any:
        return self.dict_decode[self.data[i]]

    def filter_eq(self, value: Any) -> List[int]:
        if value not in self.dict_encode:
            return []
        code = self.dict_encode[value]
        return [i for i, c in enumerate(self.data) if c == code]


class ColumnStore:
    def __init__(self):
        self.columns: Dict[str, Column] = {}
        self.nrows = 0

    def add_column(self, name: str) -> Column:
        col = Column(name)
        self.columns[name] = col
        return col

    def insert_row(self, row: Dict[str, Any]) -> None:
        for name, col in self.columns.items():
            col.append(row.get(name))
        self.nrows += 1


if __name__ == "__main__":
    cs = ColumnStore()
    cs.add_column("city")
    cs.add_column("age")
    cs.insert_row({"city": "NYC", "age": 30})
    cs.insert_row({"city": "LA", "age": 25})
    cs.insert_row({"city": "NYC", "age": 40})
    assert cs.columns["city"].filter_eq("NYC") == [0, 2]
    print("column_store self-tests passed")
