"""Softmax and log-softmax (numerically stable).

Complexity: O(n).
Original implementation.
"""
from __future__ import annotations

import numpy as np


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Numerically stable softmax along axis."""
    x = np.asarray(x, dtype=float)
    shifted = x - np.max(x, axis=axis, keepdims=True)
    exp_x = np.exp(shifted)
    return exp_x / np.sum(exp_x, axis=axis, keepdims=True)


def log_softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Numerically stable log-softmax along axis."""
    x = np.asarray(x, dtype=float)
    shifted = x - np.max(x, axis=axis, keepdims=True)
    return shifted - np.log(np.sum(np.exp(shifted), axis=axis, keepdims=True))


if __name__ == "__main__":
    x = np.array([1.0, 2.0, 3.0])
    s = softmax(x)
    assert abs(s.sum() - 1.0) < 1e-12
    assert s[2] > s[1] > s[0]
    # large values stability
    s2 = softmax(np.array([1000.0, 1001.0, 1002.0]))
    assert abs(s2.sum() - 1.0) < 1e-12
    ls = log_softmax(x)
    assert np.allclose(np.exp(ls), s)
    print("softmax self-tests passed")
