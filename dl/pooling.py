"""Max and average pooling 2D."""
from __future__ import annotations
from typing import List


class MaxPool2d:
    def __init__(self, kernel_size: int = 2, stride: int = None):
        self.k = kernel_size
        self.stride = stride or kernel_size

    def __call__(self, x: List[List[List[float]]]) -> List[List[List[float]]]:
        C, H, W = len(x), len(x[0]), len(x[0][0])
        H_out = (H - self.k) // self.stride + 1
        W_out = (W - self.k) // self.stride + 1
        out = [[[0.0] * W_out for _ in range(H_out)] for _ in range(C)]
        for c in range(C):
            for oh in range(H_out):
                for ow in range(W_out):
                    m = float("-inf")
                    for kh in range(self.k):
                        for kw in range(self.k):
                            m = max(m, x[c][oh * self.stride + kh][ow * self.stride + kw])
                    out[c][oh][ow] = m
        return out

    def parameters(self):
        return []


class AvgPool2d:
    def __init__(self, kernel_size: int = 2, stride: int = None):
        self.k = kernel_size
        self.stride = stride or kernel_size

    def __call__(self, x: List[List[List[float]]]) -> List[List[List[float]]]:
        C, H, W = len(x), len(x[0]), len(x[0][0])
        H_out = (H - self.k) // self.stride + 1
        W_out = (W - self.k) // self.stride + 1
        out = [[[0.0] * W_out for _ in range(H_out)] for _ in range(C)]
        area = self.k * self.k
        for c in range(C):
            for oh in range(H_out):
                for ow in range(W_out):
                    s = 0.0
                    for kh in range(self.k):
                        for kw in range(self.k):
                            s += x[c][oh * self.stride + kh][ow * self.stride + kw]
                    out[c][oh][ow] = s / area
        return out

    def parameters(self):
        return []


if __name__ == "__main__":
    x = [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]]
    out = MaxPool2d(2)(x)
    assert out[0][0][0] == 6
    print(f"pooling {out}")
    print("pooling self-tests passed")
