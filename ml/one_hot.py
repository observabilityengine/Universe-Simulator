"""One-hot encoding / decoding.

Complexity: O(n * c).
Original implementation with NumPy.
"""
from __future__ import annotations

import numpy as np
from typing import List


def one_hot_encode(labels: List[int], num_classes: int | None = None) -> np.ndarray:
    """labels: class indices. Returns (n, c) array."""
    if not labels:
        c = num_classes or 0
        return np.zeros((0, c))
    mx = max(labels)
    c = num_classes if num_classes is not None else mx + 1
    if c <= mx:
        raise ValueError("num_classes too small")
    out = np.zeros((len(labels), c))
    for i, lab in enumerate(labels):
        if lab < 0 or lab >= c:
            raise ValueError(f"label {lab} out of range")
        out[i, lab] = 1.0
    return out


def one_hot_decode(matrix: np.ndarray) -> List[int]:
    """Argmax along last axis."""
    matrix = np.asarray(matrix)
    if matrix.size == 0:
        return []
    return list(np.argmax(matrix, axis=-1))


if __name__ == "__main__":
    enc = one_hot_encode([0, 2, 1], num_classes=3)
    assert enc.shape == (3, 3)
    assert enc[0, 0] == 1 and enc[1, 2] == 1
    assert one_hot_decode(enc) == [0, 2, 1]
    assert one_hot_encode([]) .shape[0] == 0
    print("one_hot self-tests passed")
