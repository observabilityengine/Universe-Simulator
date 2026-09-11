"""Tree-walk interpreter."""
from __future__ import annotations
from typing import Any, Dict
from .ast import Number, Name, BinOp, UnaryOp, Assign, Call, Return, Block, If, Function
from .parser import parse


class Interpreter:
    def __init__(self):
        self.env: Dict[str, Any] = {}
        self.functions: Dict[str, Function] = {}

    def eval(self, node: Any) -> Any:
        if isinstance(node, Number):
            return node.value
        if isinstance(node, Name):
            if node.id not in self.env:
                raise NameError(node.id)
            return self.env[node.id]
        if isinstance(node, BinOp):
            l, r = self.eval(node.left), self.eval(node.right)
            ops = {
                "+": lambda a, b: a + b, "-": lambda a, b: a - b,
                "*": lambda a, b: a * b, "/": lambda a, b: a / b,
                "==": lambda a, b: a == b, "!=": lambda a, b: a != b,
                "<": lambda a, b: a < b, ">": lambda a, b: a > b,
            }
            return ops[node.op](l, r)
        if isinstance(node, UnaryOp):
            v = self.eval(node.operand)
            return -v if node.op == "-" else not v
        if isinstance(node, Assign):
            val = self.eval(node.value)
            self.env[node.target] = val
            return val
        if isinstance(node, Block):
            result = None
            for stmt in node.statements:
                result = self.eval(stmt)
                if isinstance(stmt, Return):
                    return result
            return result
        if isinstance(node, Return):
            return self.eval(node.value)
        if isinstance(node, Call):
            if node.func in self.functions:
                fn = self.functions[node.func]
                args = [self.eval(a) for a in node.args]
                saved = self.env.copy()
                for p, a in zip(fn.params, args):
                    self.env[p] = a
                result = None
                for stmt in fn.body:
                    result = self.eval(stmt)
                    if isinstance(stmt, Return):
                        break
                self.env = saved
                return result
            raise NameError(f"Unknown function {node.func}")
        return None

    def run(self, source: str) -> Any:
        tree = parse(source)
        return self.eval(tree)


if __name__ == "__main__":
    interp = Interpreter()
    assert interp.run("1 + 2 * 3") == 7
    interp.run("let x = 10")
    assert interp.env["x"] == 10
    print("interpreter self-tests passed")
