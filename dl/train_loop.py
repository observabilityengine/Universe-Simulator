"""Generic training loop."""
from __future__ import annotations
from typing import Callable, List, Tuple
from .tensor import Tensor
from .sgd_optimizer import SGD
from .mse_loss import mse_loss


def train(
    model,
    data: List[Tuple[Tensor, Tensor]],
    epochs: int = 50,
    lr: float = 0.05,
    loss_fn: Callable = mse_loss,
) -> List[float]:
    opt = SGD(model.parameters(), lr=lr)
    history = []
    for epoch in range(epochs):
        total_loss = 0.0
        for x, y in data:
            opt.zero_grad()
            pred = model(x)
            loss = loss_fn(pred, y)
            loss.backward()
            opt.step()
            total_loss += loss.data[0][0]
        history.append(total_loss / len(data))
    return history


if __name__ == "__main__":
    from .mlp import MLP
    model = MLP([1, 8, 1], seed=1)
    data = [(Tensor([[float(i)]]), Tensor([[float(i * 2)]])) for i in range(10)]
    hist = train(model, data, epochs=30, lr=0.01)
    assert hist[-1] < hist[0]
    print(f"train_loop loss {hist[0]:.3f} -> {hist[-1]:.3f}")
    print("train_loop self-tests passed")
