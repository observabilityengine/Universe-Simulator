"""Mean squared error loss."""
from __future__ import annotations
from .tensor import Tensor


def mse_loss(pred: Tensor, target: Tensor) -> Tensor:
    diff = pred + (target * Tensor([[-1.0]]))
    return (diff * diff).sum() * Tensor([[1.0 / (pred.shape[0] * pred.shape[1])]])


if __name__ == "__main__":
    p = Tensor([[1.0, 2.0]], requires_grad=True)
    t = Tensor([[1.0, 1.0]])
    loss = mse_loss(p, t)
    loss.backward()
    assert p.grad is not None
    print(f"mse_loss {loss.data[0][0]:.4f}")
    print("mse_loss self-tests passed")
