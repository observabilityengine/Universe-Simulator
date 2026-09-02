"""
Module 9 – Observability Engine
Structured logging, counters, gauges, and simple tracing.
Fully functional. Original implementation.
"""

from __future__ import annotations
import time
import json
import threading
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from contextlib import contextmanager


@dataclass
class LogRecord:
    timestamp: float
    level: str
    logger: str
    message: str
    data: Dict[str, Any] = field(default_factory=dict)


class Metrics:
    def __init__(self):
        self._counters: Dict[str, int] = defaultdict(int)
        self._gauges: Dict[str, float] = {}
        self._lock = threading.Lock()

    def inc(self, name: str, value: int = 1) -> None:
        with self._lock:
            self._counters[name] += value

    def set_gauge(self, name: str, value: float) -> None:
        with self._lock:
            self._gauges[name] = value

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {"counters": dict(self._counters), "gauges": dict(self._gauges)}


class Tracer:
    def __init__(self):
        self._spans: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    @contextmanager
    def span(self, name: str, **attrs: Any):
        start = time.time()
        span_data = {"name": name, "start": start, "attrs": attrs}
        try:
            yield span_data
        finally:
            span_data["end"] = time.time()
            span_data["duration"] = span_data["end"] - start
            with self._lock:
                self._spans.append(span_data)

    def get_spans(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._spans)


class ObservabilityEngine:
    def __init__(self, name: str = "universe", max_logs: int = 5000):
        self.name = name
        self.max_logs = max_logs
        self._logs: List[LogRecord] = []
        self._lock = threading.Lock()
        self.metrics = Metrics()
        self.tracer = Tracer()

    def log(self, level: str, message: str, **data: Any) -> None:
        rec = LogRecord(timestamp=time.time(), level=level.upper(), logger=self.name, message=message, data=data)
        with self._lock:
            self._logs.append(rec)
            if len(self._logs) > self.max_logs:
                self._logs = self._logs[-self.max_logs:]

    def info(self, message: str, **data: Any) -> None:
        self.log("INFO", message, **data)

    def warn(self, message: str, **data: Any) -> None:
        self.log("WARN", message, **data)

    def error(self, message: str, **data: Any) -> None:
        self.log("ERROR", message, **data)

    def recent_logs(self, n: int = 20) -> List[Dict]:
        with self._lock:
            return [asdict(l) for l in self._logs[-n:]]

    def report(self) -> Dict[str, Any]:
        return {"logger": self.name, "log_count": len(self._logs), "metrics": self.metrics.snapshot(), "spans": len(self.tracer.get_spans()), "recent": self.recent_logs(5)}


if __name__ == "__main__":
    print("Testing Observability Engine...")
    obs = ObservabilityEngine("test")
    obs.info("System starting", version="1.0")
    obs.metrics.inc("events_processed", 3)
    obs.metrics.set_gauge("temperature", 298.15)
    with obs.tracer.span("compute", size=100):
        time.sleep(0.01)
    obs.warn("Low memory", free_mb=128)
    print(json.dumps(obs.report(), indent=2, default=str))
    print("Observability Engine module OK.")
