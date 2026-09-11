"""Simple static type checker for numeric expressions."""
from __future__ import annotations
from typing import Any, Dict
from .ast import Number, Name, BinOp, Assign, Block


def type_check(node: Any, env: Dict[str, str] = None) -> str:
    env = env if env is not None else {}
    if isinstance(node, Number):
        return "float"
    if isinstance(node, Name):
        return env.get(node.id, "float")
    if isinstance(node, BinOp):
        lt = type_check(node.left, env)
        rt = type_check(node.right, env)
        if lt != rt:
            raise TypeError(f"Type mismatch {lt} {node.op} {rt}")
        return lt
    if isinstance(node, Assign):
        t = type_check(node.value, env)
        env[node.target] = t
        return t
    if isinstance(node, Block):
        for stmt in node.statements:
            type_check(stmt, env)
        return "void"
    return "float"


if __name__ == "__main__":
    from .parser import parse
    t = type_check(parse("1 + 2"))
    assert t == "float"
    print("type_checker self-tests passed")
