"""Symbolic expression tree – numbers, variables, operators."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Union


@dataclass(frozen=True)
class Num:
    value: float
    def __repr__(self):
        return str(self.value)


@dataclass(frozen=True)
class Var:
    name: str
    def __repr__(self):
        return self.name


@dataclass(frozen=True)
class Op:
    op: str
    args: tuple
    def __repr__(self):
        if len(self.args) == 2:
            return f"({self.args[0]} {self.op} {self.args[1]})"
        return f"{self.op}({', '.join(map(str, self.args))})"


Expr = Union[Num, Var, Op]


def evaluate(expr: Expr, env: Dict[str, float]) -> float:
    if isinstance(expr, Num):
        return expr.value
    if isinstance(expr, Var):
        return env[expr.name]
    if isinstance(expr, Op):
        vals = [evaluate(a, env) for a in expr.args]
        if expr.op == "+":
            return vals[0] + vals[1]
        if expr.op == "-":
            return vals[0] - vals[1] if len(vals) == 2 else -vals[0]
        if expr.op == "*":
            return vals[0] * vals[1]
        if expr.op == "/":
            return vals[0] / vals[1]
        if expr.op == "**":
            return vals[0] ** vals[1]
        if expr.op == "sin":
            import math
            return math.sin(vals[0])
        if expr.op == "cos":
            import math
            return math.cos(vals[0])
    raise ValueError(expr)


if __name__ == "__main__":
    e = Op("+", (Op("*", (Num(2), Var("x"))), Num(3)))
    assert evaluate(e, {"x": 5}) == 13
    print(f"expression {e} = {evaluate(e, {'x': 5})}")
    print("expression self-tests passed")
