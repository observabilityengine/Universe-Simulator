"""Constant folding optimization."""
from __future__ import annotations
from typing import Any
from .ast import Number, BinOp, UnaryOp, Block, Assign


def fold_constants(node: Any) -> Any:
    if isinstance(node, BinOp):
        left = fold_constants(node.left)
        right = fold_constants(node.right)
        if isinstance(left, Number) and isinstance(right, Number):
            ops = {"+": left.value + right.value, "-": left.value - right.value,
                   "*": left.value * right.value, "/": left.value / right.value if right.value else float("nan")}
            if node.op in ops:
                return Number(ops[node.op])
        return BinOp(left, node.op, right)
    if isinstance(node, UnaryOp):
        operand = fold_constants(node.operand)
        if isinstance(operand, Number) and node.op == "-":
            return Number(-operand.value)
        return UnaryOp(node.op, operand)
    if isinstance(node, Block):
        return Block([fold_constants(s) for s in node.statements])
    if isinstance(node, Assign):
        return Assign(node.target, fold_constants(node.value))
    return node


if __name__ == "__main__":
    from .parser import parse
    tree = fold_constants(parse("1 + 2"))
    assert isinstance(tree, Number) and tree.value == 3
    print("constant_folding self-tests passed")
