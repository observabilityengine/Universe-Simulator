"""Minimal transformer language model block (pure Python)."""
from __future__ import annotations
import math
import random
from typing import List


def softmax(xs: List[float]) -> List[float]:
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps) or 1.0
    return [e / s for e in exps]


def attention(Q: List[List[float]], K: List[List[float]], V: List[List[float]]) -> List[List[float]]:
    n, d = len(Q), len(Q[0])
    scale = 1.0 / math.sqrt(d)
    out = []
    for i in range(n):
        scores = [sum(Q[i][k] * K[j][k] for k in range(d)) * scale for j in range(n)]
        weights = softmax(scores)
        row = [sum(weights[j] * V[j][k] for j in range(n)) for k in range(d)]
        out.append(row)
    return out


def transformer_block(x: List[List[float]], seed: int = 42) -> List[List[float]]:
    rng = random.Random(seed)
    n, d = len(x), len(x[0])
    # toy projections = identity + noise
    Q = [[x[i][j] + rng.gauss(0, 0.01) for j in range(d)] for i in range(n)]
    K = [[x[i][j] + rng.gauss(0, 0.01) for j in range(d)] for i in range(n)]
    V = [row[:] for row in x]
    attn = attention(Q, K, V)
    # residual
    return [[attn[i][j] + x[i][j] for j in range(d)] for i in range(n)]


if __name__ == "__main__":
    x = [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]]
    out = transformer_block(x)
    assert len(out) == 3 and len(out[0]) == 2
    print(f"transformer_lm out[0]={out[0]}")
    print("transformer_lm self-tests passed")
