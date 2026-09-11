"""Adam optimizer."""
from __future__ import annotations
import math
from typing import List
from .tensor import Tensor


class Adam:
    def __init__(self, params: List[Tensor], lr: float = 0.001, betas=(0.9, 0.999), eps: float = 1e-8):
        self.params = params
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.m = [p._zeros() for p in params]
        self.v = [p._zeros() for p in params]
        self.t = 0

    def step(self) -> None:
        self.t += 1
        for i, p in enumerate(self.params):
            if p.grad is None:
                continue
            for r in range(p.shape[0]):
                for c in range(p.shape[1]):
                    g = p.grad[r][c]
                    self.m[i][r][c] = self.beta1 * self.m[i][r][c] + (1 - self.beta1) * g
                    self.v[i][r][c] = self.beta2 * self.v[i][r][c] + (1 - self.beta2) * g * g
                    mhat = self.m[i][r][c] / (1 - self.beta1 ** self.t)
                    vhat = self.v[i][r][c] / (1 - self.beta2 ** self.t)
                    p.data[r][c] -= self.lr * mhat / (math.sqrt(vhat) + self.eps)

    def zero_grad(self) -> None:
        for p in self.params:
            p.zero_grad()


if __name__ == "__main__":
    from .linear_layer import Linear
    from .mse_loss import mse_loss
    layer = Linear(2, 1, seed=2)
    opt = Adam(layer.parameters(), lr=0.05)
    x = Tensor([[1.0, 0.5]])
    target = Tensor([[1.0]])
    for _ in range(30):
        opt.zero_grad()
        loss = mse_loss(layer(x), target)
        loss.backward()
        opt.step()
    print(f"adam_optimizer final_loss={loss.data[0][0]:.4f}")
    print("adam_optimizer self-tests passed")
