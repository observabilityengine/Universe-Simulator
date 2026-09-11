"""Lexer for a minimal expression language."""
from __future__ import annotations
from typing import List, Tuple

Token = Tuple[str, str]


def tokenize(source: str) -> List[Token]:
    tokens: List[Token] = []
    i, n = 0, len(source)
    while i < n:
        c = source[i]
        if c.isspace():
            i += 1
            continue
        if c.isdigit() or (c == "." and i + 1 < n and source[i + 1].isdigit()):
            j = i
            while j < n and (source[j].isdigit() or source[j] == "."):
                j += 1
            tokens.append(("NUMBER", source[i:j]))
            i = j
            continue
        if c.isalpha() or c == "_":
            j = i
            while j < n and (source[j].isalnum() or source[j] == "_"):
                j += 1
            word = source[i:j]
            if word in ("let", "if", "else", "fn", "return", "true", "false"):
                tokens.append(("KEYWORD", word))
            else:
                tokens.append(("IDENT", word))
            i = j
            continue
        if c in "+-*/=<>!(){},;":
            if c in ("=", "!", "<", ">") and i + 1 < n and source[i + 1] == "=":
                tokens.append(("OP", c + "="))
                i += 2
            else:
                tokens.append(("OP" if c in "+-*/=<>!" else "PUNCT", c))
                i += 1
            continue
        raise SyntaxError(f"Unexpected char: {c!r} at {i}")
    tokens.append(("EOF", ""))
    return tokens


if __name__ == "__main__":
    toks = tokenize("let x = 1 + 2")
    assert toks[0] == ("KEYWORD", "let")
    assert any(t[0] == "NUMBER" for t in toks)
    print(f"lexer tokens={toks[:5]}")
    print("lexer self-tests passed")
