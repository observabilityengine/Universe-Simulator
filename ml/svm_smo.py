"""
Universe Simulator - Linear SVM via SMO (simplified)
Original sequential minimal optimization for hard-margin approximation.
"""

from __future__ import annotations

from typing import List, Tuple

class LinearSVM:
    def __init__(self, C: float = 1.0, tol: float = 1e-3, max_passes: int = 20):
        self.C = C
        self.tol = tol
        self.max_passes = max_passes
        self.w: List[float] = []
        self.b = 0.0

    def fit(self, X: List[List[float]], y: List[int]) -> None:
        n, d = len(X), len(X[0])
        alpha = [0.0] * n
        self.b = 0.0
        passes = 0
        while passes < self.max_passes:
            changed = 0
            for i in range(n):
                ei = self._predict_raw(X[i], alpha, X, y) - y[i]
                if (y[i] * ei < -self.tol and alpha[i] < self.C) or (y[i] * ei > self.tol and alpha[i] > 0):
                    j = (i + 1) % n
                    ej = self._predict_raw(X[j], alpha, X, y) - y[j]
                    ai_old, aj_old = alpha[i], alpha[j]
                    if y[i] != y[j]:
                        L = max(0.0, alpha[j] - alpha[i])
                        H = min(self.C, self.C + alpha[j] - alpha[i])
                    else:
                        L = max(0.0, alpha[i] + alpha[j] - self.C)
                        H = min(self.C, alpha[i] + alpha[j])
                    if L == H:
                        continue
                    eta = 2 * self._dot(X[i], X[j]) - self._dot(X[i], X[i]) - self._dot(X[j], X[j])
                    if eta >= 0:
                        continue
                    alpha[j] -= y[j] * (ei - ej) / eta
                    alpha[j] = max(L, min(H, alpha[j]))
                    if abs(alpha[j] - aj_old) < 1e-5:
                        continue
                    alpha[i] += y[i] * y[j] * (aj_old - alpha[j])
                    b1 = self.b - ei - y[i] * (alpha[i] - ai_old) * self._dot(X[i], X[i]) - y[j] * (alpha[j] - aj_old) * self._dot(X[i], X[j])
                    b2 = self.b - ej - y[i] * (alpha[i] - ai_old) * self._dot(X[i], X[j]) - y[j] * (alpha[j] - aj_old) * self._dot(X[j], X[j])
                    self.b = (b1 + b2) / 2
                    changed += 1
            if changed == 0:
                passes += 1
            else:
                passes = 0
        self.w = [0.0] * d
        for i in range(n):
            for k in range(d):
                self.w[k] += alpha[i] * y[i] * X[i][k]

    def _dot(self, a: List[float], b: List[float]) -> float:
        return sum(x * y for x, y in zip(a, b))

    def _predict_raw(self, x: List[float], alpha: List[float], X: List[List[float]], y: List[int]) -> float:
        s = self.b
        for i in range(len(X)):
            s += alpha[i] * y[i] * self._dot(X[i], x)
        return s

    def predict(self, x: List[float]) -> int:
        return 1 if sum(w * xi for w, xi in zip(self.w, x)) + self.b >= 0 else -1

if __name__ == "__main__":
    X = [[0.0, 0.0], [0.1, 0.1], [1.0, 1.0], [1.1, 0.9]]
    y = [-1, -1, 1, 1]
    svm = LinearSVM(C=1.0, max_passes=10)
    svm.fit(X, y)
    assert svm.predict([0.05, 0.05]) == -1
    assert svm.predict([1.05, 1.0]) == 1
    print("svm_smo self-test passed")
