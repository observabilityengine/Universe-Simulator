"""AST optimizer pipeline."""
from __future__ import annotations
from typing import Any
from .constant_folding import fold_constants
from .dead_code_elimination import eliminate_dead_code


def optimize(node: Any) -> Any:
    node = fold_constants(node)
    node = eliminate_dead_code(node)
    return node


if __name__ == "__main__":
    from .parser import parse
    from .interpreter import Interpreter
    tree = parse("1 + 2 * 3")
    opt = optimize(tree)
    assert Interpreter().eval(opt) == 7
    print("optimizer self-tests passed")
