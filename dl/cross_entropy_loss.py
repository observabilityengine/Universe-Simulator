"""Cross-entropy loss with logits."""
from __future__ import annotations
import math
from .tensor import Tensor
from .softmax import softmax


def cross_entropy(pred: Tensor, target_idx: int) -> Tensor:
    """pred: (1, C) logits, target_idx: class index."""
    probs = softmax(pred)
    p = max(probs.data[0][target_idx], 1e-12)
    loss_val = -math.log(p)
    out = Tensor([[loss_val]], requires_grad=pred.requires_grad, _parents=(pred,), _op="ce")
    def _backward():
        if pred.requires_grad:
            if pred.grad is None: pred.grad = pred._zeros()
            for j in range(pred.shape[1]):
                pred.grad[0][j] += (probs.data[0][j] - (1.0 if j == target_idx else 0.0)) * out.grad[0][0]
    out._backward = _backward
    return out


if __name__ == "__main__":
    logits = Tensor([[2.0, 1.0, 0.1]], requires_grad=True)
    loss = cross_entropy(logits, 0)
    loss.backward()
    assert logits.grad is not None
    print(f"cross_entropy_loss {loss.data[0][0]:.4f}")
    print("cross_entropy_loss self-tests passed")
