"""
Module 17 – Pure NumPy Neural Network
Multi-layer perceptron with backprop, trained from scratch.
Original, executable implementation. No external ML libraries.
"""

from __future__ import annotations
import numpy as np
from typing import List, Tuple, Optional


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0.0, x)


def relu_grad(x: np.ndarray) -> np.ndarray:
    return (x > 0).astype(float)


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def sigmoid_grad(x: np.ndarray) -> np.ndarray:
    s = sigmoid(x)
    return s * (1.0 - s)


class NeuralNet:
    def __init__(self, layer_sizes: List[int], activation: str = "relu", seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed)
        self.layer_sizes = layer_sizes
        self.activation = activation
        self.weights: List[np.ndarray] = []
        self.biases: List[np.ndarray] = []
        for i in range(len(layer_sizes) - 1):
            w = self.rng.normal(0, np.sqrt(2.0 / layer_sizes[i]), size=(layer_sizes[i], layer_sizes[i + 1]))
            b = np.zeros(layer_sizes[i + 1])
            self.weights.append(w)
            self.biases.append(b)

    def _act(self, x: np.ndarray) -> np.ndarray:
        return relu(x) if self.activation == "relu" else sigmoid(x)

    def _act_grad(self, x: np.ndarray) -> np.ndarray:
        return relu_grad(x) if self.activation == "relu" else sigmoid_grad(x)

    def forward(self, x: np.ndarray) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        activations = [x]
        pre_acts = []
        a = x
        for w, b in zip(self.weights, self.biases):
            z = a @ w + b
            pre_acts.append(z)
            a = self._act(z)
            activations.append(a)
        return activations, pre_acts

    def predict(self, x: np.ndarray) -> np.ndarray:
        acts, _ = self.forward(x)
        return acts[-1]

    def train_step(self, x: np.ndarray, y: np.ndarray, lr: float = 0.01) -> float:
        acts, pre = self.forward(x)
        err = acts[-1] - y
        loss = np.mean(err ** 2)
        delta = err * self._act_grad(pre[-1])
        grads_w = []
        grads_b = []
        for i in reversed(range(len(self.weights))):
            grads_w.append(acts[i].T @ delta / len(x))
            grads_b.append(np.mean(delta, axis=0))
            if i > 0:
                delta = (delta @ self.weights[i].T) * self._act_grad(pre[i - 1])
        grads_w.reverse()
        grads_b.reverse()
        for i in range(len(self.weights)):
            self.weights[i] -= lr * grads_w[i]
            self.biases[i] -= lr * grads_b[i]
        return float(loss)

    def fit(self, x: np.ndarray, y: np.ndarray, epochs: int = 500, lr: float = 0.05) -> List[float]:
        losses = []
        for ep in range(epochs):
            loss = self.train_step(x, y, lr)
            losses.append(loss)
        return losses


if __name__ == "__main__":
    print("Testing Pure NumPy Neural Net...")
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    Y = np.array([[0], [1], [1], [0]], dtype=float)
    net = NeuralNet([2, 8, 1], activation="sigmoid", seed=42)
    losses = net.fit(X, Y, epochs=2000, lr=0.5)
    preds = net.predict(X)
    print("  XOR targets:", Y.ravel())
    print("  XOR preds:  ", np.round(preds.ravel(), 3))
    print(f"  Final loss: {losses[-1]:.6f}")
    print("Neural Net module OK.")
