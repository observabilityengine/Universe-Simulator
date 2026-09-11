"""LSTM cell."""
from __future__ import annotations
from typing import Tuple
from .tensor import Tensor, randn
from .sigmoid import sigmoid


class LSTMCell:
    def __init__(self, input_size: int, hidden_size: int, seed: int = 42):
        self.hidden_size = hidden_size
        self.W_ii = randn(input_size, hidden_size, requires_grad=True, seed=seed)
        self.W_hi = randn(hidden_size, hidden_size, requires_grad=True, seed=seed+1)
        self.W_if = randn(input_size, hidden_size, requires_grad=True, seed=seed+2)
        self.W_hf = randn(hidden_size, hidden_size, requires_grad=True, seed=seed+3)
        self.W_ig = randn(input_size, hidden_size, requires_grad=True, seed=seed+4)
        self.W_hg = randn(hidden_size, hidden_size, requires_grad=True, seed=seed+5)
        self.W_io = randn(input_size, hidden_size, requires_grad=True, seed=seed+6)
        self.W_ho = randn(hidden_size, hidden_size, requires_grad=True, seed=seed+7)

    def __call__(self, x: Tensor, state: Tuple[Tensor, Tensor] = None) -> Tuple[Tensor, Tensor]:
        if state is None:
            h = Tensor([[0.0] * self.hidden_size])
            c = Tensor([[0.0] * self.hidden_size])
        else:
            h, c = state
        i = sigmoid(x @ self.W_ii + h @ self.W_hi)
        f = sigmoid(x @ self.W_if + h @ self.W_hf)
        g = (x @ self.W_ig + h @ self.W_hg).relu()  # tanh approx with relu for simplicity
        o = sigmoid(x @ self.W_io + h @ self.W_ho)
        c_new = f * c + i * g
        h_new = o * c_new.relu()
        return h_new, c_new

    def parameters(self):
        return [self.W_ii, self.W_hi, self.W_if, self.W_hf, self.W_ig, self.W_hg, self.W_io, self.W_ho]


if __name__ == "__main__":
    cell = LSTMCell(3, 4)
    x = Tensor([[1.0, 0.0, 0.0]])
    h, c = cell(x)
    assert h.shape == (1, 4)
    print("lstm self-tests passed")
