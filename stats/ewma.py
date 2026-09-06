"""Exponentially weighted moving average (EWMA).

Complexity: O(n) for n observations.
Online and batch interfaces. Original implementation.
"""
from __future__ import annotations

from typing import List, Sequence


def ewma(values: Sequence[float], alpha: float) -> List[float]:
    """Batch EWMA. alpha in (0, 1]; higher alpha = more weight on recent."""
    if not (0 < alpha <= 1):
        raise ValueError("alpha must be in (0, 1]")
    if not values:
        return []
    out: List[float] = []
    s = float(values[0])
    out.append(s)
    for x in values[1:]:
        s = alpha * x + (1 - alpha) * s
        out.append(s)
    return out


class EWMA:
    """Online EWMA tracker."""

    def __init__(self, alpha: float) -> None:
        if not (0 < alpha <= 1):
            raise ValueError("alpha must be in (0, 1]")
        self.alpha = alpha
        self.value: float | None = None

    def update(self, x: float) -> float:
        if self.value is None:
            self.value = x
        else:
            self.value = self.alpha * x + (1 - self.alpha) * self.value
        return self.value


if __name__ == "__main__":
    vals = [1.0, 2.0, 3.0, 4.0, 5.0]
    out = ewma(vals, 0.5)
    assert len(out) == 5
    assert abs(out[0] - 1.0) < 1e-12
    assert abs(out[-1] - 4.0625) < 1e-10
    e = EWMA(0.5)
    assert e.update(1.0) == 1.0
    assert abs(e.update(3.0) - 2.0) < 1e-12
    assert ewma([], 0.5) == []
    try:
        ewma([1], 0.0)
        assert False
    except ValueError:
        pass
    print("ewma self-tests passed")
