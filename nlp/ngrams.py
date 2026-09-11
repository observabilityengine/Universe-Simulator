"""N-gram generation."""
from __future__ import annotations
from typing import List, Tuple


def ngrams(tokens: List[str], n: int = 2) -> List[Tuple[str, ...]]:
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def ngram_counts(tokens: List[str], n: int = 2) -> dict:
    counts: dict = {}
    for g in ngrams(tokens, n):
        counts[g] = counts.get(g, 0) + 1
    return counts


if __name__ == "__main__":
    toks = ["a", "b", "c", "a", "b"]
    bg = ngrams(toks, 2)
    assert ("a", "b") in bg
    print(f"ngrams {bg}")
    print("ngrams self-tests passed")
