"""Symbol table with nested scopes."""
from __future__ import annotations
from typing import Any, Dict, Optional


class SymbolTable:
    def __init__(self, parent: Optional["SymbolTable"] = None):
        self.parent = parent
        self.symbols: Dict[str, Any] = {}

    def define(self, name: str, value: Any = None) -> None:
        self.symbols[name] = value

    def resolve(self, name: str) -> Any:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.resolve(name)
        raise NameError(name)

    def child(self) -> "SymbolTable":
        return SymbolTable(parent=self)


if __name__ == "__main__":
    global_ = SymbolTable()
    global_.define("x", 1)
    local = global_.child()
    local.define("y", 2)
    assert local.resolve("x") == 1
    assert local.resolve("y") == 2
    print("symbol_table self-tests passed")
