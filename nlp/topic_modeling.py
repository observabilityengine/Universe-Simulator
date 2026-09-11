"""Latent Dirichlet Allocation – simplified collapsed Gibbs."""
from __future__ import annotations
import random
from collections import defaultdict
from typing import Dict, List, Tuple


def lda_gibbs(
    docs: List[List[str]],
    n_topics: int = 2,
    n_iter: int = 20,
    alpha: float = 0.1,
    beta: float = 0.1,
    seed: int = 42,
) -> Tuple[List[List[int]], Dict[int, Dict[str, int]]]:
    rng = random.Random(seed)
    vocab = sorted({w for d in docs for w in d})
    word2id = {w: i for i, w in enumerate(vocab)}
    # topic assignments
    z = [[rng.randrange(n_topics) for _ in doc] for doc in docs]
    n_dk = [[0] * n_topics for _ in docs]
    n_kw: List[Dict[str, int]] = [defaultdict(int) for _ in range(n_topics)]
    n_k = [0] * n_topics
    for d, doc in enumerate(docs):
        for i, w in enumerate(doc):
            t = z[d][i]
            n_dk[d][t] += 1
            n_kw[t][w] += 1
            n_k[t] += 1
    V = len(vocab)
    for _ in range(n_iter):
        for d, doc in enumerate(docs):
            for i, w in enumerate(doc):
                t = z[d][i]
                n_dk[d][t] -= 1
                n_kw[t][w] -= 1
                n_k[t] -= 1
                probs = []
                for k in range(n_topics):
                    p = (n_dk[d][k] + alpha) * (n_kw[k][w] + beta) / (n_k[k] + V * beta)
                    probs.append(p)
                total = sum(probs) or 1
                r = rng.random() * total
                cum = 0.0
                new_t = 0
                for k, p in enumerate(probs):
                    cum += p
                    if r <= cum:
                        new_t = k
                        break
                z[d][i] = new_t
                n_dk[d][new_t] += 1
                n_kw[new_t][w] += 1
                n_k[new_t] += 1
    return z, n_kw


if __name__ == "__main__":
    docs = [["cat", "cat", "dog"], ["dog", "dog", "cat"], ["apple", "banana", "apple"]]
    z, topics = lda_gibbs(docs, n_topics=2, n_iter=10)
    assert len(z) == 3
    print(f"topic_modeling topics={[{k: dict(v) for k, v in enumerate(topics)}]}")
    print("topic_modeling self-tests passed")
