"""Categorical cross-entropy loss (numerically stable).

Complexity: O(n * c) for n samples, c classes.
Supports one-hot or class-index labels. Original implementation.
"""
from __future__ import annotations

import numpy as np


def cross_entropy(
    probs: np.ndarray,
    targets: np.ndarray,
    eps: float = 1e-12,
) -> float:
    """Mean CE. probs (n, c) probabilities; targets (n,) indices or (n, c) one-hot."""
    probs = np.asarray(probs, dtype=float)
    targets = np.asarray(targets)
    probs = np.clip(probs, eps, 1.0 - eps)
    if targets.ndim == 1:
        n = probs.shape[0]
        return float(-np.mean(np.log(probs[np.arange(n), targets.astype(int)])))
    return float(-np.mean(np.sum(targets * np.log(probs), axis=-1)))


if __name__ == "__main__":
    probs = np.array([[0.7, 0.2, 0.1], [0.1, 0.5, 0.4]])
    loss = cross_entropy(probs, np.array([0, 1]))
    assert loss > 0
    # perfect prediction
    perfect = np.array([[1.0, 0.0], [0.0, 1.0]])
    assert cross_entropy(perfect, np.array([0, 1])) < 1e-10
    print("cross_entropy self-tests passed")
