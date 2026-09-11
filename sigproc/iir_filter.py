"""Generic IIR difference equation filter."""
from __future__ import annotations
from typing import List


class IIRFilter:
    def __init__(self, b: List[float], a: List[float]):
        """y[n] = b[0]*x[n] + b[1]*x[n-1] + ... - a[1]*y[n-1] - ...
        a[0] is assumed 1 (normalized).
        """
        self.b = list(b)
        self.a = list(a)
        if self.a and abs(self.a[0] - 1.0) > 1e-12:
            s = self.a[0]
            self.b = [v / s for v in self.b]
            self.a = [v / s for v in self.a]
        self.xs = [0.0] * len(self.b)
        self.ys = [0.0] * len(self.a)

    def process(self, x: float) -> float:
        self.xs = [x] + self.xs[:-1]
        y = sum(bi * xi for bi, xi in zip(self.b, self.xs))
        y -= sum(ai * yi for ai, yi in zip(self.a[1:], self.ys[:-1]))
        self.ys = [y] + self.ys[:-1]
        return y

    def process_block(self, data: List[float]) -> List[float]:
        return [self.process(v) for v in data]


if __name__ == "__main__":
    # simple exponential smoother: y = 0.5*x + 0.5*y_prev
    f = IIRFilter([0.5], [1.0, -0.5])
    out = f.process_block([1.0] * 5)
    assert out[-1] > out[0]
    print(f"iir_filter {out}")
    print("iir_filter self-tests passed")
