"""Sequential container for layers."""
from __future__ import annotations
from typing import List
from .tensor import Tensor


class Sequential:
    def __init__(self, *layers):
        self.layers = list(layers)

    def __call__(self, x: Tensor) -> Tensor:
        for layer in self.layers:
            x = layer(x)
        return x

    def parameters(self) -> List[Tensor]:
        params = []
        for layer in self.layers:
            if hasattr(layer, "parameters"):
                params.extend(layer.parameters())
        return params


if __name__ == "__main__":
    from .linear_layer import Linear
    from .relu import ReLU
    model = Sequential(Linear(3, 4), ReLU(), Linear(4, 1))
    x = Tensor([[1.0, 0.0, -1.0]])
    y = model(x)
    assert y.shape == (1, 1)
    print(f"sequential out={y.data}")
    print("sequential self-tests passed")
