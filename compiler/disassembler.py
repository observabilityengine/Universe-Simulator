"""Bytecode disassembler."""
from __future__ import annotations
from typing import List, Tuple


def disassemble(code: List[Tuple[str, object]]) -> str:
    lines = []
    for i, (op, arg) in enumerate(code):
        lines.append(f"{i:4d} {op:12s} {arg}")
    return "\n".join(lines)


if __name__ == "__main__":
    code = [("LOAD_CONST", 1), ("LOAD_CONST", 2), ("BINARY_OP", "+")]
    text = disassemble(code)
    assert "LOAD_CONST" in text
    print(text)
    print("disassembler self-tests passed")
