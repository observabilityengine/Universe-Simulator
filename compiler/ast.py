"""AST node definitions."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Union


@dataclass
class Number:
    value: float


@dataclass
class Name:
    id: str


@dataclass
class BinOp:
    left: Any
    op: str
    right: Any


@dataclass
class UnaryOp:
    op: str
    operand: Any


@dataclass
class Assign:
    target: str
    value: Any


@dataclass
class Call:
    func: str
    args: List[Any]


@dataclass
class If:
    test: Any
    body: List[Any]
    orelse: List[Any]


@dataclass
class Function:
    name: str
    params: List[str]
    body: List[Any]


@dataclass
class Return:
    value: Any


@dataclass
class Block:
    statements: List[Any]


if __name__ == "__main__":
    n = Number(42)
    assert n.value == 42
    b = BinOp(Number(1), "+", Number(2))
    assert b.op == "+"
    print("ast self-tests passed")
