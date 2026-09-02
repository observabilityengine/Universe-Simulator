"""
Universe Simulator - Lightweight Metrics Collector
Original counters, gauges, histograms for observability.
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from typing import Dict, List


class Metrics:
    def __init__(self) -> None:
        self._counters: Dict[str, float] = defaultdict(float)
        self._gauges: Dict[str, float] = {}
        self._hist: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def inc(self, name: str, value: float = 1.0) -> None:
        with self._lock:
            self._counters[name] += value

    def set_gauge(self, name: str, value: float) -> None:
        with self._lock:
            self._gauges[name] = value

    def observe(self, name: str, value: float) -> None:
        with self._lock:
            self._hist[name].append(value)

    def snapshot(self) -> Dict[str, object]:
        with self._lock:
            return {
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": {k: list(v) for k, v in self._hist.items()},
            }

    def reset(self) -> None:
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._hist.clear()


if __name__ == "__main__":
    m = Metrics()
    m.inc("frames")
    m.inc("frames", 2)
    m.set_gauge("fps", 60.0)
    m.observe("latency", 0.012)
    snap = m.snapshot()
    assert snap["counters"]["frames"] == 3.0
    assert snap["gauges"]["fps"] == 60.0
    print("metrics self-test passed", snap)
