"""Bytecode instruction set and compiler from AST."""
from __future__ import annotations
from typing import Any, List, Tuple
from .ast import Number, Name, BinOp, Assign, Block

Op = Tuple[str, Any]


def compile_ast(node: Any) -> List[Op]:
    code: List[Op] = []
    if isinstance(node, Number):
        code.append(("LOAD_CONST", node.value))
    elif isinstance(node, Name):
        code.append(("LOAD_NAME", node.id))
    elif isinstance(node, BinOp):
        code.extend(compile_ast(node.left))
        code.extend(compile_ast(node.right))
        code.append(("BINARY_OP", node.op))
    elif isinstance(node, Assign):
        code.extend(compile_ast(node.value))
        code.append(("STORE_NAME", node.target))
    elif isinstance(node, Block):
        for stmt in node.statements:
            code.extend(compile_ast(stmt))
    return code


def run_bytecode(code: List[Op], env: dict = None) -> Any:
    env = env if env is not None else {}
    stack = []
    for op, arg in code:
        if op == "LOAD_CONST":
            stack.append(arg)
        elif op == "LOAD_NAME":
            stack.append(env[arg])
        elif op == "STORE_NAME":
            env[arg] = stack.pop()
        elif op == "BINARY_OP":
            r, l = stack.pop(), stack.pop()
            ops = {"+": l + r, "-": l - r, "*": l * r, "/": l / r}
            stack.append(ops[arg])
    return stack[-1] if stack else None


if __name__ == "__main__":
    from .parser import parse
    code = compile_ast(parse("1 + 2"))
    assert run_bytecode(code) == 3
    print(f"bytecode {code}")
    print("bytecode self-tests passed")
