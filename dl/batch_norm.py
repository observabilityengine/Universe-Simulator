"""Batch normalization (1D)."""
from __future__ import annotations
from .tensor import Tensor


class BatchNorm1d:
    def __init__(self, num_features: int, eps: float = 1e-5, momentum: float = 0.1):
        self.eps = eps
        self.momentum = momentum
        self.gamma = Tensor([[1.0] * num_features], requires_grad=True)
        self.beta = Tensor([[0.0] * num_features], requires_grad=True)
        self.running_mean = [0.0] * num_features
        self.running_var = [1.0] * num_features
        self.training = True

    def __call__(self, x: Tensor) -> Tensor:
        r, c = x.shape
        if self.training:
            mean = [sum(x.data[i][j] for i in range(r)) / r for j in range(c)]
            var = [sum((x.data[i][j] - mean[j]) ** 2 for i in range(r)) / r for j in range(c)]
            for j in range(c):
                self.running_mean[j] = (1 - self.momentum) * self.running_mean[j] + self.momentum * mean[j]
                self.running_var[j] = (1 - self.momentum) * self.running_var[j] + self.momentum * var[j]
        else:
            mean, var = self.running_mean, self.running_var
        data = [[(x.data[i][j] - mean[j]) / ((var[j] + self.eps) ** 0.5) * self.gamma.data[0][j] + self.beta.data[0][j] for j in range(c)] for i in range(r)]
        return Tensor(data, requires_grad=x.requires_grad)

    def parameters(self):
        return [self.gamma, self.beta]


if __name__ == "__main__":
    bn = BatchNorm1d(3)
    x = Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    y = bn(x)
    assert y.shape == (2, 3)
    print(f"batch_norm {y.data[0]}")
    print("batch_norm self-tests passed")
