"""Minimal JIT: compile expression AST to Python function via exec."""
from __future__ import annotations
from typing import Any, Callable
from .codegen import codegen
from .parser import parse


def jit_compile(source: str) -> Callable:
    tree = parse(source)
    py = codegen(tree)
    ns: dict = {}
    exec(f"def _fn():\n    return {py}", ns)
    return ns["_fn"]


if __name__ == "__main__":
    fn = jit_compile("1 + 2 * 3")
    assert fn() == 7
    print("jit_compiler self-tests passed")
