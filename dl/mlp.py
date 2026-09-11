"""Multi-layer perceptron."""
from __future__ import annotations
from .sequential import Sequential
from .linear_layer import Linear
from .relu import ReLU


def MLP(sizes: list, seed: int = 42) -> Sequential:
    layers = []
    for i in range(len(sizes) - 1):
        layers.append(Linear(sizes[i], sizes[i + 1], seed=seed + i))
        if i < len(sizes) - 2:
            layers.append(ReLU())
    return Sequential(*layers)


if __name__ == "__main__":
    model = MLP([2, 8, 1])
    from .tensor import Tensor
    y = model(Tensor([[0.5, -0.5]]))
    assert y.shape == (1, 1)
    print(f"mlp out={y.data}")
    print("mlp self-tests passed")
