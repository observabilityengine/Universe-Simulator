"""Tensor with reverse-mode autograd."""
from __future__ import annotations
import math
import random
from typing import Any, Callable, List, Optional, Tuple, Union

Number = Union[int, float]


class Tensor:
    __slots__ = ("data", "grad", "requires_grad", "_parents", "_op", "_backward")

    def __init__(self, data: Any, requires_grad: bool = False, _parents: Tuple = (), _op: str = ""):
        if isinstance(data, (int, float)):
            self.data = [[float(data)]]
        elif isinstance(data, list):
            if data and isinstance(data[0], (int, float)):
                self.data = [[float(x) for x in data]]
            else:
                self.data = [[float(x) for x in row] for row in data]
        else:
            self.data = data
        self.grad: Optional[List[List[float]]] = None
        self.requires_grad = requires_grad
        self._parents = _parents
        self._op = _op
        self._backward: Callable = lambda: None

    @property
    def shape(self) -> Tuple[int, int]:
        return (len(self.data), len(self.data[0]) if self.data else 0)

    def _zeros(self) -> List[List[float]]:
        r, c = self.shape
        return [[0.0] * c for _ in range(r)]

    def zero_grad(self) -> None:
        self.grad = self._zeros()

    def backward(self) -> None:
        if self.grad is None:
            self.grad = [[1.0] * self.shape[1] for _ in range(self.shape[0])]
        topo = []
        visited = set()
        def build(v):
            if id(v) not in visited:
                visited.add(id(v))
                for p in v._parents:
                    build(p)
                topo.append(v)
        build(self)
        for v in reversed(topo):
            v._backward()

    def __add__(self, other: Any) -> "Tensor":
        other = other if isinstance(other, Tensor) else Tensor(other)
        r, c = self.shape
        data = [[self.data[i][j] + other.data[min(i, other.shape[0]-1)][min(j, other.shape[1]-1)] for j in range(c)] for i in range(r)]
        out = Tensor(data, requires_grad=self.requires_grad or other.requires_grad, _parents=(self, other), _op="+")
        def _backward():
            if self.requires_grad:
                if self.grad is None: self.grad = self._zeros()
                for i in range(r):
                    for j in range(c):
                        self.grad[i][j] += out.grad[i][j]
            if other.requires_grad:
                if other.grad is None: other.grad = other._zeros()
                for i in range(r):
                    for j in range(c):
                        other.grad[min(i, other.shape[0]-1)][min(j, other.shape[1]-1)] += out.grad[i][j]
        out._backward = _backward
        return out

    def __mul__(self, other: Any) -> "Tensor":
        other = other if isinstance(other, Tensor) else Tensor(other)
        r, c = self.shape
        data = [[self.data[i][j] * other.data[min(i, other.shape[0]-1)][min(j, other.shape[1]-1)] for j in range(c)] for i in range(r)]
        out = Tensor(data, requires_grad=self.requires_grad or other.requires_grad, _parents=(self, other), _op="*")
        def _backward():
            if self.requires_grad:
                if self.grad is None: self.grad = self._zeros()
                for i in range(r):
                    for j in range(c):
                        self.grad[i][j] += other.data[min(i, other.shape[0]-1)][min(j, other.shape[1]-1)] * out.grad[i][j]
            if other.requires_grad:
                if other.grad is None: other.grad = other._zeros()
                for i in range(r):
                    for j in range(c):
                        other.grad[min(i, other.shape[0]-1)][min(j, other.shape[1]-1)] += self.data[i][j] * out.grad[i][j]
        out._backward = _backward
        return out

    def __matmul__(self, other: "Tensor") -> "Tensor":
        r, k = self.shape
        k2, c = other.shape
        assert k == k2
        data = [[sum(self.data[i][kk] * other.data[kk][j] for kk in range(k)) for j in range(c)] for i in range(r)]
        out = Tensor(data, requires_grad=self.requires_grad or other.requires_grad, _parents=(self, other), _op="@")
        def _backward():
            if self.requires_grad:
                if self.grad is None: self.grad = self._zeros()
                for i in range(r):
                    for kk in range(k):
                        for j in range(c):
                            self.grad[i][kk] += other.data[kk][j] * out.grad[i][j]
            if other.requires_grad:
                if other.grad is None: other.grad = other._zeros()
                for kk in range(k):
                    for j in range(c):
                        for i in range(r):
                            other.grad[kk][j] += self.data[i][kk] * out.grad[i][j]
        out._backward = _backward
        return out

    def relu(self) -> "Tensor":
        r, c = self.shape
        data = [[max(0.0, self.data[i][j]) for j in range(c)] for i in range(r)]
        out = Tensor(data, requires_grad=self.requires_grad, _parents=(self,), _op="relu")
        def _backward():
            if self.requires_grad:
                if self.grad is None: self.grad = self._zeros()
                for i in range(r):
                    for j in range(c):
                        self.grad[i][j] += (1.0 if self.data[i][j] > 0 else 0.0) * out.grad[i][j]
        out._backward = _backward
        return out

    def sum(self) -> "Tensor":
        total = sum(sum(row) for row in self.data)
        out = Tensor([[total]], requires_grad=self.requires_grad, _parents=(self,), _op="sum")
        def _backward():
            if self.requires_grad:
                if self.grad is None: self.grad = self._zeros()
                g = out.grad[0][0]
                for i in range(self.shape[0]):
                    for j in range(self.shape[1]):
                        self.grad[i][j] += g
        out._backward = _backward
        return out

    def __repr__(self) -> str:
        return f"Tensor(shape={self.shape}, requires_grad={self.requires_grad})"


def randn(rows: int, cols: int, requires_grad: bool = False, seed: int = None) -> Tensor:
    rng = random.Random(seed)
    return Tensor([[rng.gauss(0, 1) for _ in range(cols)] for _ in range(rows)], requires_grad=requires_grad)


if __name__ == "__main__":
    a = Tensor([[1.0, 2.0], [3.0, 4.0]], requires_grad=True)
    b = Tensor([[0.5], [1.5]], requires_grad=True)
    c = (a @ b).sum()
    c.backward()
    assert a.grad is not None
    print(f"tensor grad={a.grad}")
    print("tensor self-tests passed")
