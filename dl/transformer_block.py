"""Transformer encoder block (simplified)."""
from __future__ import annotations
from .tensor import Tensor, randn
from .attention import scaled_dot_product_attention
from .linear_layer import Linear
from .relu import ReLU


class TransformerBlock:
    def __init__(self, d_model: int, seed: int = 42):
        self.W_q = Linear(d_model, d_model, seed=seed)
        self.W_k = Linear(d_model, d_model, seed=seed + 1)
        self.W_v = Linear(d_model, d_model, seed=seed + 2)
        self.ff1 = Linear(d_model, d_model * 2, seed=seed + 3)
        self.ff2 = Linear(d_model * 2, d_model, seed=seed + 4)
        self.relu = ReLU()

    def __call__(self, x: Tensor) -> Tensor:
        Q, K, V = self.W_q(x), self.W_k(x), self.W_v(x)
        attn = scaled_dot_product_attention(Q, K, V)
        x = x + attn
        ff = self.ff2(self.relu(self.ff1(x)))
        return x + ff

    def parameters(self):
        params = []
        for layer in (self.W_q, self.W_k, self.W_v, self.ff1, self.ff2):
            params.extend(layer.parameters())
        return params


if __name__ == "__main__":
    block = TransformerBlock(4)
    x = Tensor([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]])
    out = block(x)
    assert out.shape == (2, 4)
    print("transformer_block self-tests passed")
