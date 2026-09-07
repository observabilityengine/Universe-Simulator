"""CART decision tree for classification and regression.

Complexity: O(n features * n samples * depth). Original implementation.
"""
from __future__ import annotations

from typing import Any, List, Optional, Tuple
import math


class Node:
    __slots__ = ("feature", "threshold", "left", "right", "value", "n_samples")

    def __init__(self) -> None:
        self.feature: Optional[int] = None
        self.threshold: Optional[float] = None
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.value: Any = None
        self.n_samples: int = 0


def _gini(y: List[int]) -> float:
    if not y:
        return 0.0
    counts: dict[int, int] = {}
    for v in y:
        counts[v] = counts.get(v, 0) + 1
    n = len(y)
    return 1.0 - sum((c / n) ** 2 for c in counts.values())


def _mse(y: List[float]) -> float:
    if not y:
        return 0.0
    mean = sum(y) / len(y)
    return sum((v - mean) ** 2 for v in y) / len(y)


def _majority(y: List[int]) -> int:
    counts: dict[int, int] = {}
    for v in y:
        counts[v] = counts.get(v, 0) + 1
    return max(counts, key=counts.get)  # type: ignore


def _mean(y: List[float]) -> float:
    return sum(y) / len(y) if y else 0.0


def _best_split(
    X: List[List[float]], y: List[Any], task: str, min_samples_leaf: int,
) -> Tuple[Optional[int], Optional[float], float]:
    n, d = len(X), len(X[0])
    best_gain = -1.0
    best_feat, best_thr = None, None
    parent_imp = _gini(y) if task == "classification" else _mse(y)
    for feat in range(d):
        values = sorted(set(row[feat] for row in X))
        for i in range(len(values) - 1):
            thr = (values[i] + values[i + 1]) / 2.0
            left_y = [y[j] for j in range(n) if X[j][feat] <= thr]
            right_y = [y[j] for j in range(n) if X[j][feat] > thr]
            if len(left_y) < min_samples_leaf or len(right_y) < min_samples_leaf:
                continue
            if task == "classification":
                imp = (len(left_y) * _gini(left_y) + len(right_y) * _gini(right_y)) / n
            else:
                imp = (len(left_y) * _mse(left_y) + len(right_y) * _mse(right_y)) / n
            gain = parent_imp - imp
            if gain > best_gain:
                best_gain = gain
                best_feat = feat
                best_thr = thr
    return best_feat, best_thr, best_gain


def _build(
    X: List[List[float]], y: List[Any], task: str, max_depth: int,
    min_samples_split: int, min_samples_leaf: int, depth: int,
) -> Node:
    node = Node()
    node.n_samples = len(y)
    node.value = _majority(y) if task == "classification" else _mean(y)
    if depth >= max_depth or len(y) < min_samples_split or len(set(y)) == 1:
        return node
    feat, thr, gain = _best_split(X, y, task, min_samples_leaf)
    if feat is None or gain <= 0:
        return node
    left_idx = [i for i in range(len(X)) if X[i][feat] <= thr]
    right_idx = [i for i in range(len(X)) if X[i][feat] > thr]
    if len(left_idx) < min_samples_leaf or len(right_idx) < min_samples_leaf:
        return node
    node.feature = feat
    node.threshold = thr
    node.left = _build([X[i] for i in left_idx], [y[i] for i in left_idx], task, max_depth, min_samples_split, min_samples_leaf, depth + 1)
    node.right = _build([X[i] for i in right_idx], [y[i] for i in right_idx], task, max_depth, min_samples_split, min_samples_leaf, depth + 1)
    return node


def _predict_one(node: Node, x: List[float]) -> Any:
    while node.feature is not None:
        if x[node.feature] <= node.threshold:  # type: ignore
            node = node.left  # type: ignore
        else:
            node = node.right  # type: ignore
    return node.value


class CART:
    def __init__(self, task: str = "classification", max_depth: int = 10, min_samples_split: int = 2, min_samples_leaf: int = 1) -> None:
        assert task in ("classification", "regression")
        self.task = task
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.root: Optional[Node] = None

    def fit(self, X: List[List[float]], y: List[Any]) -> "CART":
        self.root = _build(X, y, self.task, self.max_depth, self.min_samples_split, self.min_samples_leaf, 0)
        return self

    def predict(self, X: List[List[float]]) -> List[Any]:
        assert self.root is not None
        return [_predict_one(self.root, x) for x in X]


if __name__ == "__main__":
    Xc = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
    yc = [0, 0, 0, 1]
    tree = CART(task="classification", max_depth=3).fit(Xc, yc)
    assert tree.predict(Xc) == yc
    Xr = [[float(i)] for i in range(10)]
    yr = [float(i) for i in range(10)]
    reg = CART(task="regression", max_depth=5).fit(Xr, yr)
    pred_r = reg.predict([[3.0], [7.0]])
    assert abs(pred_r[0] - 3.0) < 1.5
    assert abs(pred_r[1] - 7.0) < 1.5
    print("cart self-tests passed")
