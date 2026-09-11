"""Code generation to Python source."""
from __future__ import annotations
from typing import Any
from .ast import Number, Name, BinOp, Assign, Block


def codegen(node: Any) -> str:
    if isinstance(node, Number):
        return str(node.value)
    if isinstance(node, Name):
        return node.id
    if isinstance(node, BinOp):
        return f"({codegen(node.left)} {node.op} {codegen(node.right)})"
    if isinstance(node, Assign):
        return f"{node.target} = {codegen(node.value)}"
    if isinstance(node, Block):
        return "\n".join(codegen(s) for s in node.statements)
    return "None"


if __name__ == "__main__":
    from .parser import parse
    src = codegen(parse("1 + 2"))
    assert "1" in src and "2" in src
    print(f"codegen {src}")
    print("codegen self-tests passed")
