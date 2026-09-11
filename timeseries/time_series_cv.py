"""Time-series cross-validation splits."""
from __future__ import annotations
from typing import Iterator, List, Tuple


def rolling_origin_splits(
    n: int, min_train: int = 10, horizon: int = 1, step: int = 1
) -> Iterator[Tuple[range, range]]:
    start = min_train
    while start + horizon <= n:
        yield range(0, start), range(start, start + horizon)
        start += step


def expanding_window_splits(
    n: int, n_splits: int = 5, horizon: int = 1
) -> Iterator[Tuple[range, range]]:
    test_size = (n - horizon) // n_splits
    for i in range(n_splits):
        train_end = test_size * (i + 1)
        yield range(0, train_end), range(train_end, min(train_end + horizon, n))


if __name__ == "__main__":
    splits = list(rolling_origin_splits(30, 10, 3, 5))
    assert len(splits) >= 3
    print(f"time_series_cv n_splits={len(splits)}")
    print("time_series_cv self-tests passed")
