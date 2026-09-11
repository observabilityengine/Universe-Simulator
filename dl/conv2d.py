"""2D convolution layer (pure Python)."""
from __future__ import annotations
from typing import List
from .tensor import Tensor, randn


class Conv2d:
    def __init__(self, in_ch: int, out_ch: int, kernel_size: int = 3, stride: int = 1, seed: int = 42):
        self.in_ch = in_ch
        self.out_ch = out_ch
        self.k = kernel_size
        self.stride = stride
        self.weight = randn(out_ch, in_ch * kernel_size * kernel_size, requires_grad=True, seed=seed)
        scale = (2.0 / (in_ch * kernel_size * kernel_size)) ** 0.5
        self.weight.data = [[w * scale for w in row] for row in self.weight.data]
        self.bias = Tensor([[0.0] * out_ch], requires_grad=True)

    def __call__(self, x: List[List[List[float]]]) -> List[List[List[float]]]:
        """x: C x H x W list. Returns out_ch x H' x W'."""
        C, H, W = len(x), len(x[0]), len(x[0][0])
        H_out = (H - self.k) // self.stride + 1
        W_out = (W - self.k) // self.stride + 1
        out = [[[0.0] * W_out for _ in range(H_out)] for _ in range(self.out_ch)]
        for oc in range(self.out_ch):
            for oh in range(H_out):
                for ow in range(W_out):
                    s = self.bias.data[0][oc]
                    idx = 0
                    for ic in range(self.in_ch):
                        for kh in range(self.k):
                            for kw in range(self.k):
                                s += x[ic][oh * self.stride + kh][ow * self.stride + kw] * self.weight.data[oc][idx]
                                idx += 1
                    out[oc][oh][ow] = s
        return out

    def parameters(self):
        return [self.weight, self.bias]


if __name__ == "__main__":
    conv = Conv2d(1, 2, 3, seed=1)
    x = [[[0.0]*5 for _ in range(5)]]
    x[0][2][2] = 1.0
    out = conv(x)
    assert len(out) == 2
    print(f"conv2d out_shape={len(out)}x{len(out[0])}x{len(out[0][0])}")
    print("conv2d self-tests passed")
