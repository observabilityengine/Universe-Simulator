"""Symbolic differentiation."""
from __future__ import annotations
from .expression import Expr, Num, Var, Op


def diff(expr: Expr, var: str) -> Expr:
    if isinstance(expr, Num):
        return Num(0)
    if isinstance(expr, Var):
        return Num(1 if expr.name == var else 0)
    if isinstance(expr, Op):
        if expr.op == "+":
            return Op("+", (diff(expr.args[0], var), diff(expr.args[1], var)))
        if expr.op == "-":
            if len(expr.args) == 1:
                return Op("-", (diff(expr.args[0], var),))
            return Op("-", (diff(expr.args[0], var), diff(expr.args[1], var)))
        if expr.op == "*":
            u, v = expr.args
            return Op("+", (Op("*", (diff(u, var), v)), Op("*", (u, diff(v, var)))))
        if expr.op == "/":
            u, v = expr.args
            num = Op("-", (Op("*", (diff(u, var), v)), Op("*", (u, diff(v, var)))))
            den = Op("*", (v, v))
            return Op("/", (num, den))
        if expr.op == "**":
            base, exp = expr.args
            if isinstance(exp, Num):
                return Op("*", (Op("*", (exp, Op("**", (base, Num(exp.value - 1))))), diff(base, var)))
        if expr.op == "sin":
            return Op("*", (Op("cos", (expr.args[0],)), diff(expr.args[0], var)))
        if expr.op == "cos":
            return Op("*", (Op("-", (Op("sin", (expr.args[0],)),)), diff(expr.args[0], var)))
    raise ValueError(expr)


if __name__ == "__main__":
    from .expression import evaluate
    e = Op("**", (Var("x"), Num(3)))
    d = diff(e, "x")
    assert abs(evaluate(d, {"x": 2}) - 12) < 1e-9
    print(f"differentiate d/dx(x^3)={d}")
    print("differentiate self-tests passed")
