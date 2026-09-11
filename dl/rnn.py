"""Vanilla RNN cell."""
from __future__ import annotations
from typing import List, Tuple
from .tensor import Tensor, randn


class RNNCell:
    def __init__(self, input_size: int, hidden_size: int, seed: int = 42):
        self.hidden_size = hidden_size
        self.W_ih = randn(input_size, hidden_size, requires_grad=True, seed=seed)
        self.W_hh = randn(hidden_size, hidden_size, requires_grad=True, seed=seed + 1)
        self.bias = Tensor([[0.0] * hidden_size], requires_grad=True)

    def __call__(self, x: Tensor, h: Tensor = None) -> Tensor:
        if h is None:
            h = Tensor([[0.0] * self.hidden_size])
        return (x @ self.W_ih + h @ self.W_hh + self.bias).relu()

    def parameters(self):
        return [self.W_ih, self.W_hh, self.bias]


if __name__ == "__main__":
    cell = RNNCell(4, 8)
    x = Tensor([[1.0, 0.0, 0.0, 0.0]])
    h = cell(x)
    assert h.shape == (1, 8)
    print(f"rnn h={h.shape}")
    print("rnn self-tests passed")
