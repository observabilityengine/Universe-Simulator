"""Algebraic simplification rules."""
from __future__ import annotations
from .expression import Expr, Num, Var, Op


def simplify(expr: Expr) -> Expr:
    if isinstance(expr, (Num, Var)):
        return expr
    if isinstance(expr, Op):
        args = tuple(simplify(a) for a in expr.args)
        if expr.op == "+":
            a, b = args
            if isinstance(a, Num) and a.value == 0:
                return b
            if isinstance(b, Num) and b.value == 0:
                return a
            if isinstance(a, Num) and isinstance(b, Num):
                return Num(a.value + b.value)
        if expr.op == "*":
            a, b = args
            if isinstance(a, Num) and a.value == 0:
                return Num(0)
            if isinstance(b, Num) and b.value == 0:
                return Num(0)
            if isinstance(a, Num) and a.value == 1:
                return b
            if isinstance(b, Num) and b.value == 1:
                return a
            if isinstance(a, Num) and isinstance(b, Num):
                return Num(a.value * b.value)
        if expr.op == "-":
            if len(args) == 1 and isinstance(args[0], Num):
                return Num(-args[0].value)
            if len(args) == 2 and isinstance(args[0], Num) and isinstance(args[1], Num):
                return Num(args[0].value - args[1].value)
        if expr.op == "**":
            a, b = args
            if isinstance(b, Num) and b.value == 0:
                return Num(1)
            if isinstance(b, Num) and b.value == 1:
                return a
            if isinstance(a, Num) and isinstance(b, Num):
                return Num(a.value ** b.value)
        return Op(expr.op, args)
    return expr


if __name__ == "__main__":
    e = Op("+", (Op("*", (Num(0), Var("x"))), Num(5)))
    s = simplify(e)
    assert isinstance(s, Num) and s.value == 5
    print(f"simplify {e} -> {s}")
    print("simplify self-tests passed")
