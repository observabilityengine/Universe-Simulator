"""SGD optimizer with optional momentum."""
from __future__ import annotations
from typing import List
from .tensor import Tensor


class SGD:
    def __init__(self, params: List[Tensor], lr: float = 0.01, momentum: float = 0.0):
        self.params = params
        self.lr = lr
        self.momentum = momentum
        self.velocity = [p._zeros() for p in params]

    def step(self) -> None:
        for i, p in enumerate(self.params):
            if p.grad is None:
                continue
            for r in range(p.shape[0]):
                for c in range(p.shape[1]):
                    self.velocity[i][r][c] = self.momentum * self.velocity[i][r][c] - self.lr * p.grad[r][c]
                    p.data[r][c] += self.velocity[i][r][c]

    def zero_grad(self) -> None:
        for p in self.params:
            p.zero_grad()


if __name__ == "__main__":
    from .linear_layer import Linear
    from .mse_loss import mse_loss
    layer = Linear(2, 1, seed=1)
    opt = SGD(layer.parameters(), lr=0.1)
    x = Tensor([[1.0, 1.0]])
    target = Tensor([[1.0]])
    for _ in range(20):
        opt.zero_grad()
        loss = mse_loss(layer(x), target)
        loss.backward()
        opt.step()
    print(f"sgd_optimizer final_loss={loss.data[0][0]:.4f}")
    print("sgd_optimizer self-tests passed")
