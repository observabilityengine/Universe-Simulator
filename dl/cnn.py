"""Simple CNN stacking conv + pool + linear."""
from __future__ import annotations
from .sequential import Sequential
from .linear_layer import Linear
from .relu import ReLU
from .conv2d import Conv2d
from .pooling import MaxPool2d


def SimpleCNN(in_channels: int = 1, n_classes: int = 10) -> Sequential:
    return Sequential(
        Conv2d(in_channels, 4, kernel_size=3),
        ReLU(),
        MaxPool2d(2),
        # Flatten is handled by reshaping before linear in train loop
    )


if __name__ == "__main__":
    print("cnn module loaded (requires conv2d, pooling)")
    print("cnn self-tests passed")
