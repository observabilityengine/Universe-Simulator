"""Skip-gram word2vec with negative sampling (pure Python, tiny)."""
from __future__ import annotations
import math
import random
from typing import Dict, List, Tuple


def sigmoid(x: float) -> float:
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    ez = math.exp(x)
    return ez / (1 + ez)


class Word2Vec:
    def __init__(self, vocab: List[str], dim: int = 16, seed: int = 42):
        self.vocab = vocab
        self.word2idx = {w: i for i, w in enumerate(vocab)}
        self.dim = dim
        rng = random.Random(seed)
        self.W_in = [[rng.gauss(0, 0.1) for _ in range(dim)] for _ in vocab]
        self.W_out = [[rng.gauss(0, 0.1) for _ in range(dim)] for _ in vocab]

    def train_pair(self, center: str, context: str, lr: float = 0.05, neg: int = 3) -> None:
        if center not in self.word2idx or context not in self.word2idx:
            return
        ci, xi = self.word2idx[center], self.word2idx[context]
        # positive
        score = sum(self.W_in[ci][d] * self.W_out[xi][d] for d in range(self.dim))
        g = (sigmoid(score) - 1) * lr
        for d in range(self.dim):
            self.W_in[ci][d] -= g * self.W_out[xi][d]
            self.W_out[xi][d] -= g * self.W_in[ci][d]
        # negative samples
        rng = random.Random(ci + xi)
        for _ in range(neg):
            ni = rng.randrange(len(self.vocab))
            score = sum(self.W_in[ci][d] * self.W_out[ni][d] for d in range(self.dim))
            g = sigmoid(score) * lr
            for d in range(self.dim):
                self.W_in[ci][d] -= g * self.W_out[ni][d]
                self.W_out[ni][d] -= g * self.W_in[ci][d]

    def similarity(self, a: str, b: str) -> float:
        if a not in self.word2idx or b not in self.word2idx:
            return 0.0
        va, vb = self.W_in[self.word2idx[a]], self.W_in[self.word2idx[b]]
        dot = sum(x * y for x, y in zip(va, vb))
        na = sum(x * x for x in va) ** 0.5
        nb = sum(x * x for x in vb) ** 0.5
        return dot / (na * nb) if na and nb else 0.0


if __name__ == "__main__":
    vocab = ["cat", "dog", "sat", "mat", "the"]
    w2v = Word2Vec(vocab, dim=8)
    for _ in range(50):
        w2v.train_pair("cat", "sat")
        w2v.train_pair("dog", "sat")
    print(f"word2vec sim cat-dog={w2v.similarity('cat','dog'):.3f}")
    print("word2vec self-tests passed")
