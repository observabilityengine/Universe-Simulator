"""GloVe-style co-occurrence matrix factorization (simplified)."""
from __future__ import annotations
import math
import random
from typing import Dict, List, Tuple


def build_cooccurrence(docs: List[List[str]], window: int = 2) -> Dict[Tuple[str, str], float]:
    cooc: Dict[Tuple[str, str], float] = {}
    for doc in docs:
        for i, w in enumerate(doc):
            for j in range(max(0, i - window), min(len(doc), i + window + 1)):
                if i == j:
                    continue
                key = (w, doc[j])
                cooc[key] = cooc.get(key, 0) + 1.0 / abs(i - j)
    return cooc


def glove_train(
    cooc: Dict[Tuple[str, str], float],
    vocab: List[str],
    dim: int = 8,
    n_iter: int = 30,
    seed: int = 42,
) -> Dict[str, List[float]]:
    rng = random.Random(seed)
    W = {w: [rng.gauss(0, 0.1) for _ in range(dim)] for w in vocab}
    for _ in range(n_iter):
        for (w1, w2), x in cooc.items():
            if w1 not in W or w2 not in W:
                continue
            dot = sum(W[w1][d] * W[w2][d] for d in range(dim))
            diff = dot - math.log(x + 1)
            for d in range(dim):
                g = 0.05 * diff
                W[w1][d] -= g * W[w2][d]
                W[w2][d] -= g * W[w1][d]
    return W


if __name__ == "__main__":
    docs = [["the", "cat", "sat"], ["the", "dog", "sat"]]
    cooc = build_cooccurrence(docs)
    vocab = ["the", "cat", "dog", "sat"]
    emb = glove_train(cooc, vocab, n_iter=20)
    assert len(emb["cat"]) == 8
    print("glove self-tests passed")
