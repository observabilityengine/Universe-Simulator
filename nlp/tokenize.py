"""Whitespace and simple regex tokenizer."""
from __future__ import annotations
import re
from typing import List


def tokenize(text: str, lowercase: bool = True) -> List[str]:
    if lowercase:
        text = text.lower()
    return re.findall(r"[a-z0-9']+|[.,!?;]", text)


def sent_tokenize(text: str) -> List[str]:
    return re.split(r"(?<=[.!?])\s+", text.strip())


if __name__ == "__main__":
    toks = tokenize("Hello, world! This is a test.")
    assert "hello" in toks and "," in toks
    print(f"tokenize {toks}")
    print("tokenize self-tests passed")
