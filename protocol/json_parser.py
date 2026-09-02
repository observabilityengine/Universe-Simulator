"""
Universe Simulator - Minimal Recursive Descent JSON Parser
Original pure-Python parser (no eval).
"""

from __future__ import annotations

from typing import Any, List, Tuple


class JSONParser:
    def __init__(self, text: str):
        self.text = text
        self.i = 0

    def parse(self) -> Any:
        self._skip_ws()
        val = self._value()
        self._skip_ws()
        if self.i != len(self.text):
            raise ValueError("trailing content")
        return val

    def _skip_ws(self) -> None:
        while self.i < len(self.text) and self.text[self.i] in " \t\n\r":
            self.i += 1

    def _value(self) -> Any:
        self._skip_ws()
        if self.i >= len(self.text):
            raise ValueError("unexpected end")
        c = self.text[self.i]
        if c == "n":
            return self._literal("null", None)
        if c == "t":
            return self._literal("true", True)
        if c == "f":
            return self._literal("false", False)
        if c == '"':
            return self._string()
        if c == "[":
            return self._array()
        if c == "{":
            return self._object()
        if c == "-" or c.isdigit():
            return self._number()
        raise ValueError(f"unexpected char {c}")

    def _literal(self, lit: str, val: Any) -> Any:
        if self.text[self.i:self.i+len(lit)] != lit:
            raise ValueError(f"expected {lit}")
        self.i += len(lit)
        return val

    def _string(self) -> str:
        self.i += 1
        start = self.i
        while self.i < len(self.text) and self.text[self.i] != '"':
            if self.text[self.i] == "\\":
                self.i += 2
            else:
                self.i += 1
        s = self.text[start:self.i]
        self.i += 1
        return bytes(s, "utf-8").decode("unicode_escape")

    def _number(self) -> float:
        start = self.i
        if self.text[self.i] == "-":
            self.i += 1
        while self.i < len(self.text) and self.text[self.i].isdigit():
            self.i += 1
        if self.i < len(self.text) and self.text[self.i] == ".":
            self.i += 1
            while self.i < len(self.text) and self.text[self.i].isdigit():
                self.i += 1
        return float(self.text[start:self.i])

    def _array(self) -> List[Any]:
        self.i += 1
        arr = []
        self._skip_ws()
        if self.text[self.i] == "]":
            self.i += 1
            return arr
        while True:
            arr.append(self._value())
            self._skip_ws()
            if self.text[self.i] == "]":
                self.i += 1
                return arr
            if self.text[self.i] != ",":
                raise ValueError("expected comma")
            self.i += 1

    def _object(self) -> dict:
        self.i += 1
        obj = {}
        self._skip_ws()
        if self.text[self.i] == "}":
            self.i += 1
            return obj
        while True:
            self._skip_ws()
            key = self._string()
            self._skip_ws()
            if self.text[self.i] != ":":
                raise ValueError("expected colon")
            self.i += 1
            obj[key] = self._value()
            self._skip_ws()
            if self.text[self.i] == "}":
                self.i += 1
                return obj
            if self.text[self.i] != ",":
                raise ValueError("expected comma")
            self.i += 1


if __name__ == "__main__":
    p = JSONParser('{"a": 1, "b": [true, null, "x"]}')
    result = p.parse()
    assert result == {"a": 1.0, "b": [True, None, "x"]}
    print("json_parser self-test passed", result)
