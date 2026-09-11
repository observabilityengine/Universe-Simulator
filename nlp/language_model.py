"""N-gram language model with add-k smoothing."""
from __future__ import annotations
import math
from collections import defaultdict
from typing import Dict, List, Tuple


class NgramLM:
    def __init__(self, n: int = 2, k: float = 1.0):
        self.n = n
        self.k = k
        self.counts: Dict[Tuple, int] = defaultdict(int)
        self.context_counts: Dict[Tuple, int] = defaultdict(int)
        self.vocab: set = set()

    def fit(self, tokens: List[str]) -> None:
        for t in tokens:
            self.vocab.add(t)
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i : i + self.n])
            context = ngram[:-1]
            self.counts[ngram] += 1
            self.context_counts[context] += 1

    def log_prob(self, tokens: List[str]) -> float:
        lp = 0.0
        V = len(self.vocab) or 1
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i : i + self.n])
            context = ngram[:-1]
            c = self.counts[ngram] + self.k
            total = self.context_counts[context] + self.k * V
            lp += math.log(c / total)
        return lp


if __name__ == "__main__":
    toks = ["the", "cat", "sat", "on", "the", "mat"]
    lm = NgramLM(2)
    lm.fit(toks)
    lp = lm.log_prob(["the", "cat"])
    assert lp < 0
    print(f"language_model logp={lp:.3f}")
    print("language_model self-tests passed")
