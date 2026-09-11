"""Residual block."""
from __future__ import annotations
from .tensor import Tensor
from .linear_layer import Linear
from .relu import ReLU


class ResNetBlock:
    def __init__(self, features: int, seed: int = 42):
        self.fc1 = Linear(features, features, seed=seed)
        self.fc2 = Linear(features, features, seed=seed + 1)
        self.relu = ReLU()

    def __call__(self, x: Tensor) -> Tensor:
        residual = x
        out = self.relu(self.fc1(x))
        out = self.fc2(out)
        return self.relu(out + residual)

    def parameters(self):
        return self.fc1.parameters() + self.fc2.parameters()


if __name__ == "__main__":
    block = ResNetBlock(4)
    x = Tensor([[1.0, 0.0, 0.0, 0.0]])
    out = block(x)
    assert out.shape == (1, 4)
    print("resnet_block self-tests passed")
