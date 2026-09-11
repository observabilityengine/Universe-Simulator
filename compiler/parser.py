"""Recursive-descent parser."""
from __future__ import annotations
from typing import Any, List
from .lexer import tokenize, Token
from .ast import Number, Name, BinOp, UnaryOp, Assign, Call, If, Function, Return, Block


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.current()
        self.pos += 1
        return tok

    def match(self, type_: str, value: str = None) -> bool:
        t = self.current()
        if t[0] != type_:
            return False
        if value is not None and t[1] != value:
            return False
        return True

    def parse(self) -> Any:
        stmts = []
        while not self.match("EOF"):
            stmts.append(self.statement())
        return Block(stmts) if len(stmts) != 1 else stmts[0]

    def statement(self) -> Any:
        if self.match("KEYWORD", "let"):
            self.advance()
            name = self.advance()[1]
            if self.match("OP", "="):
                self.advance()
            val = self.expression()
            if self.match("PUNCT", ";"):
                self.advance()
            return Assign(name, val)
        if self.match("KEYWORD", "return"):
            self.advance()
            val = self.expression()
            if self.match("PUNCT", ";"):
                self.advance()
            return Return(val)
        return self.expression()

    def expression(self) -> Any:
        return self.comparison()

    def comparison(self) -> Any:
        node = self.term()
        while self.match("OP") and self.current()[1] in ("==", "!=", "<", ">", "<=", ">="):
            op = self.advance()[1]
            node = BinOp(node, op, self.term())
        return node

    def term(self) -> Any:
        node = self.factor()
        while self.match("OP") and self.current()[1] in ("+", "-"):
            op = self.advance()[1]
            node = BinOp(node, op, self.factor())
        return node

    def factor(self) -> Any:
        node = self.unary()
        while self.match("OP") and self.current()[1] in ("*", "/"):
            op = self.advance()[1]
            node = BinOp(node, op, self.unary())
        return node

    def unary(self) -> Any:
        if self.match("OP") and self.current()[1] in ("-", "!"):
            op = self.advance()[1]
            return UnaryOp(op, self.unary())
        return self.primary()

    def primary(self) -> Any:
        if self.match("NUMBER"):
            return Number(float(self.advance()[1]))
        if self.match("IDENT"):
            name = self.advance()[1]
            if self.match("PUNCT", "("):
                self.advance()
                args = []
                if not self.match("PUNCT", ")"):
                    args.append(self.expression())
                    while self.match("PUNCT", ","):
                        self.advance()
                        args.append(self.expression())
                self.advance()
                return Call(name, args)
            return Name(name)
        if self.match("PUNCT", "("):
            self.advance()
            node = self.expression()
            if self.match("PUNCT", ")"):
                self.advance()
            return node
        raise SyntaxError(f"Unexpected {self.current()}")


def parse(source: str) -> Any:
    return Parser(tokenize(source)).parse()


if __name__ == "__main__":
    tree = parse("1 + 2 * 3")
    assert isinstance(tree, BinOp)
    print(f"parser {tree}")
    print("parser self-tests passed")
