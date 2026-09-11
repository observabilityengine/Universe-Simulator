"""GRU cell."""
from __future__ import annotations
from .tensor import Tensor, randn
from .sigmoid import sigmoid


class GRUCell:
    def __init__(self, input_size: int, hidden_size: int, seed: int = 42):
        self.hidden_size = hidden_size
        self.W_iz = randn(input_size, hidden_size, requires_grad=True, seed=seed)
        self.W_hz = randn(hidden_size, hidden_size, requires_grad=True, seed=seed+1)
        self.W_ir = randn(input_size, hidden_size, requires_grad=True, seed=seed+2)
        self.W_hr = randn(hidden_size, hidden_size, requires_grad=True, seed=seed+3)
        self.W_ih = randn(input_size, hidden_size, requires_grad=True, seed=seed+4)
        self.W_hh = randn(hidden_size, hidden_size, requires_grad=True, seed=seed+5)

    def __call__(self, x: Tensor, h: Tensor = None) -> Tensor:
        if h is None:
            h = Tensor([[0.0] * self.hidden_size])
        z = sigmoid(x @ self.W_iz + h @ self.W_hz)
        r = sigmoid(x @ self.W_ir + h @ self.W_hr)
        h_tilde = (x @ self.W_ih + (r * h) @ self.W_hh).relu()
        one = Tensor([[1.0] * self.hidden_size])
        return (one + z * Tensor([[-1.0]])) * h_tilde + z * h

    def parameters(self):
        return [self.W_iz, self.W_hz, self.W_ir, self.W_hr, self.W_ih, self.W_hh]


if __name__ == "__main__":
    cell = GRUCell(3, 4)
    h = cell(Tensor([[1.0, 0.0, 0.0]]))
    assert h.shape == (1, 4)
    print("gru self-tests passed")
