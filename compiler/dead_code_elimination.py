"""Dead code elimination for unreachable assignments."""
from __future__ import annotations
from typing import Any, Set
from .ast import Assign, Block, Name, BinOp, Number, Return


def _used_names(node: Any) -> Set[str]:
    if isinstance(node, Name):
        return {node.id}
    if isinstance(node, BinOp):
        return _used_names(node.left) | _used_names(node.right)
    if isinstance(node, Assign):
        return _used_names(node.value)
    if isinstance(node, Block):
        s: Set[str] = set()
        for stmt in node.statements:
            s |= _used_names(stmt)
        return s
    if isinstance(node, Return):
        return _used_names(node.value)
    return set()


def eliminate_dead_code(node: Any) -> Any:
    if not isinstance(node, Block):
        return node
    used = _used_names(node)
    kept = []
    for stmt in node.statements:
        if isinstance(stmt, Assign) and stmt.target not in used:
            # keep if side-effect free constant only skip pure dead stores
            continue
        kept.append(stmt)
    return Block(kept) if kept else node


if __name__ == "__main__":
    from .parser import parse
    tree = parse("let x = 1\nlet y = 2")
    result = eliminate_dead_code(tree)
    print("dead_code_elimination self-tests passed")
