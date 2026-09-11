"""Read-Eval-Print Loop."""
from __future__ import annotations
from .interpreter import Interpreter


def repl_eval(line: str, interp: Interpreter = None) -> str:
    interp = interp or Interpreter()
    try:
        result = interp.run(line)
        return repr(result)
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    out = repl_eval("1 + 2")
    assert "3" in out
    print(f"repl {out}")
    print("repl self-tests passed")
