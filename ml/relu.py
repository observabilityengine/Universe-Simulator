"""ReLU and variants (activation functions).

Complexity: O(n).
Original implementation with NumPy.
"""
from __future__ import annotations

import numpy as np


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0.0, np.asarray(x, dtype=float))


def relu_grad(x: np.ndarray) -> np.ndarray:
    return (np.asarray(x, dtype=float) > 0).astype(float)


def leaky_relu(x: np.ndarray, alpha: float = 0.01) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    return np.where(x > 0, x, alpha * x)


def leaky_relu_grad(x: np.ndarray, alpha: float = 0.01) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    return np.where(x > 0, 1.0, alpha)


if __name__ == "__main__":
    x = np.array([-2.0, -0.5, 0.0, 1.0, 3.0])
    y = relu(x)
    assert np.allclose(y, [0, 0, 0, 1, 3])
    assert np.allclose(relu_grad(x), [0, 0, 0, 1, 1])
    ly = leaky_relu(x, 0.1)
    assert abs(ly[0] - (-0.2)) < 1e-12
    print("relu self-tests passed")
