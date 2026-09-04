"""
Universe Simulator - Isolation Forest (anomaly detection)
Original random partitioning for outlier scores.
"""

from __future__ import annotations

import random
from typing import List, Optional, Tuple

class IsolationTree:
    def __init__(self, height_limit: int):
        self.height_limit = height_limit
        self.split_attr: Optional[int] = None
        self.split_val: Optional[float] = None
        self.left: Optional["IsolationTree"] = None
        self.right: Optional["IsolationTree"] = None
        self.size = 0

    def fit(self, X: List[List[float]], height: int = 0, rng: random.Random = None) -> None:
        self.size = len(X)
        if height >= self.height_limit or len(X) <= 1:
            return
        d = len(X[0])
        self.split_attr = rng.randint(0, d - 1)
        vals = [x[self.split_attr] for x in X]
        lo, hi = min(vals), max(vals)
        if lo == hi:
            return
        self.split_val = rng.uniform(lo, hi)
        left_x = [x for x in X if x[self.split_attr] < self.split_val]
        right_x = [x for x in X if x[self.split_attr] >= self.split_val]
        self.left = IsolationTree(self.height_limit)
        self.right = IsolationTree(self.height_limit)
        self.left.fit(left_x, height + 1, rng)
        self.right.fit(right_x, height + 1, rng)

    def path_length(self, x: List[float], height: int = 0) -> float:
        if self.left is None or self.right is None:
            return height + c_factor(self.size)
        if x[self.split_attr] < self.split_val:
            return self.left.path_length(x, height + 1)
        return self.right.path_length(x, height + 1)

def c_factor(n: int) -> float:
    if n <= 1:
        return 0.0
    return 2.0 * (math.log(n - 1) + 0.5772156649) - 2.0 * (n - 1) / n

import math

class IsolationForest:
    def __init__(self, n_trees: int = 10, sample_size: int = 64, seed: int = 42):
        self.n_trees = n_trees
        self.sample_size = sample_size
        self.rng = random.Random(seed)
        self.trees: List[IsolationTree] = []

    def fit(self, X: List[List[float]]) -> None:
        hlim = int(math.ceil(math.log2(self.sample_size)))
        self.trees = []
        for _ in range(self.n_trees):
            sample = [X[self.rng.randint(0, len(X) - 1)] for _ in range(min(self.sample_size, len(X)))]
            tree = IsolationTree(hlim)
            tree.fit(sample, rng=self.rng)
            self.trees.append(tree)

    def score(self, x: List[float]) -> float:
        avg = sum(t.path_length(x) for t in self.trees) / len(self.trees)
        return 2 ** (-avg / c_factor(self.sample_size))

if __name__ == "__main__":
    X = [[i, i] for i in range(20)] + [[100, 100]]
    clf = IsolationForest(n_trees=5, sample_size=16)
    clf.fit(X)
    assert clf.score([100, 100]) > clf.score([5, 5])
    print("isolation_forest self-test passed")
