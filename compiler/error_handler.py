"""Compiler error reporting."""
from __future__ import annotations


class CompilerError(Exception):
    def __init__(self, message: str, line: int = 0, col: int = 0):
        self.message = message
        self.line = line
        self.col = col
        super().__init__(f"[{line}:{col}] {message}")


class ErrorCollector:
    def __init__(self):
        self.errors: list = []

    def report(self, message: str, line: int = 0, col: int = 0) -> None:
        self.errors.append(CompilerError(message, line, col))

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def summary(self) -> str:
        return "\n".join(str(e) for e in self.errors)


if __name__ == "__main__":
    ec = ErrorCollector()
    ec.report("undefined variable", 1, 5)
    assert ec.has_errors()
    print(ec.summary())
    print("error_handler self-tests passed")
