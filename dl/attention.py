"""Scaled dot-product attention."""
from __future__ import annotations
import math
from typing import List
from .tensor import Tensor
from .softmax import softmax


def scaled_dot_product_attention(Q: Tensor, K: Tensor, V: Tensor) -> Tensor:
    d = Q.shape[1]
    scores = Q @ Tensor([[K.data[j][i] for j in range(K.shape[0])] for i in range(K.shape[1])])  # Q @ K.T
    # manual K.T
    KT_data = [[K.data[j][i] for j in range(K.shape[0])] for i in range(K.shape[1])]
    KT = Tensor(KT_data)
    scores = Q @ KT
    scale = 1.0 / math.sqrt(d)
    scores.data = [[v * scale for v in row] for row in scores.data]
    weights = softmax(scores)
    return weights @ V


if __name__ == "__main__":
    Q = Tensor([[1.0, 0.0], [0.0, 1.0]])
    K = Tensor([[1.0, 0.0], [0.0, 1.0]])
    V = Tensor([[1.0, 2.0], [3.0, 4.0]])
    out = scaled_dot_product_attention(Q, K, V)
    assert out.shape == (2, 2)
    print(f"attention {out.data}")
    print("attention self-tests passed")
