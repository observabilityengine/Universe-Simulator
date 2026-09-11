"""Fully-connected linear layer."""
from __future__ import annotations
from .tensor import Tensor, randn


class Linear:
    def __init__(self, in_features: int, out_features: int, bias: bool = True, seed: int = 42):
        self.weight = randn(in_features, out_features, requires_grad=True, seed=seed)
        scale = (2.0 / in_features) ** 0.5
        self.weight.data = [[w * scale for w in row] for row in self.weight.data]
        self.bias = Tensor([[0.0] * out_features], requires_grad=True) if bias else None

    def __call__(self, x: Tensor) -> Tensor:
        out = x @ self.weight
        if self.bias is not None:
            out = out + self.bias
        return out

    def parameters(self):
        params = [self.weight]
        if self.bias is not None:
            params.append(self.bias)
        return params


if __name__ == "__main__":
    layer = Linear(3, 2)
    x = Tensor([[1.0, 0.0, -1.0]])
    y = layer(x)
    assert y.shape == (1, 2)
    print(f"linear_layer out={y.data}")
    print("linear_layer self-tests passed")
