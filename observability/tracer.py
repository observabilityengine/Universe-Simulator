"""
Universe Simulator - Simple Span Tracer
Original nested span timing for observability.
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Span:
    name: str
    start: float
    end: Optional[float] = None
    children: List["Span"] = field(default_factory=list)

    @property
    def duration(self) -> float:
        if self.end is None:
            return 0.0
        return self.end - self.start


class Tracer:
    def __init__(self) -> None:
        self.root: Optional[Span] = None
        self._stack: List[Span] = []

    @contextmanager
    def span(self, name: str):
        s = Span(name=name, start=time.perf_counter())
        if self._stack:
            self._stack[-1].children.append(s)
        else:
            self.root = s
        self._stack.append(s)
        try:
            yield s
        finally:
            s.end = time.perf_counter()
            self._stack.pop()

    def report(self) -> str:
        lines: List[str] = []

        def walk(span: Span, depth: int) -> None:
            lines.append("  " * depth + f"{span.name}: {span.duration*1000:.3f} ms")
            for c in span.children:
                walk(c, depth + 1)

        if self.root:
            walk(self.root, 0)
        return "\n".join(lines)


if __name__ == "__main__":
    tr = Tracer()
    with tr.span("root"):
        with tr.span("child"):
            time.sleep(0.001)
    assert tr.root is not None and tr.root.duration > 0
    print("tracer self-test passed\n" + tr.report())
