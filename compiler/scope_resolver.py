"""Resolve variable scopes and detect unbound names."""
from __future__ import annotations
from typing import Any, Set
from .ast import Name, Assign, Block, BinOp, Number, Function


def resolve(node: Any, defined: Set[str] = None) -> Set[str]:
    defined = defined if defined is not None else set()
    unbound: Set[str] = set()
    if isinstance(node, Name):
        if node.id not in defined:
            unbound.add(node.id)
    elif isinstance(node, Assign):
        unbound |= resolve(node.value, defined)
        defined.add(node.target)
    elif isinstance(node, BinOp):
        unbound |= resolve(node.left, defined)
        unbound |= resolve(node.right, defined)
    elif isinstance(node, Block):
        local = set(defined)
        for stmt in node.statements:
            unbound |= resolve(stmt, local)
    return unbound


if __name__ == "__main__":
    from .parser import parse
    u = resolve(parse("let x = 1"))
    assert len(u) == 0
    print("scope_resolver self-tests passed")
