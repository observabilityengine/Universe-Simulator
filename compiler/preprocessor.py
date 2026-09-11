"""Source preprocessor – strip comments and normalize whitespace."""
from __future__ import annotations
import re


def preprocess(source: str) -> str:
    # Remove // line comments
    lines = []
    for line in source.splitlines():
        if "//" in line:
            line = line[: line.index("//")]
        lines.append(line)
    text = "\n".join(lines)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return text.strip()


if __name__ == "__main__":
    out = preprocess("let x = 1 // comment\n/* block */\nlet y = 2")
    assert "comment" not in out
    print(f"preprocessor {out!r}")
    print("preprocessor self-tests passed")
