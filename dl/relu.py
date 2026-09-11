"""ReLU activation."""
from __future__ import annotations
from .tensor import Tensor


def relu(x: Tensor) -> Tensor:
    return x.relu()


class ReLU:
    def __call__(self, x: Tensor) -> Tensor:
        return x.relu()

    def parameters(self):
        return []


if __name__ == "__main__":
    t = Tensor([[-1.0, 0.0, 2.0]], requires_grad=True)
    y = relu(t)
    assert y.data[0] == [0.0, 0.0, 2.0]
    y.sum().backward()
    print("relu self-tests passed")
