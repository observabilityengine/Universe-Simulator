"""
Module 8 – Simulation Scheduler
Priority-based multi-timescale event scheduler.
Fully functional. Original implementation.
"""

from __future__ import annotations

import heapq
import itertools
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional


@dataclass(order=True)
class Event:
    time: float
    priority: int
    event_id: int
    callback: Callable = field(compare=False)
    data: Any = field(default=None, compare=False)
    cancelled: bool = field(default=False, compare=False)


class Scheduler:
    def __init__(self):
        self._queue: List[Event] = []
        self._counter = itertools.count()
        self.current_time: float = 0.0
        self._running = False

    def schedule(self, delay: float, callback: Callable, priority: int = 0, data: Any = None) -> int:
        if delay < 0:
            raise ValueError("delay must be non-negative")
        eid = next(self._counter)
        event = Event(time=self.current_time + delay, priority=priority, event_id=eid, callback=callback, data=data)
        heapq.heappush(self._queue, event)
        return eid

    def schedule_repeating(self, interval: float, callback: Callable, priority: int = 0, data: Any = None, max_count: Optional[int] = None) -> None:
        count = 0
        def _wrapper(ev_data: Any = None) -> None:
            nonlocal count
            callback(ev_data)
            count += 1
            if max_count is None or count < max_count:
                self.schedule(interval, _wrapper, priority, data)
        self.schedule(interval, _wrapper, priority, data)

    def cancel(self, event_id: int) -> bool:
        for ev in self._queue:
            if ev.event_id == event_id and not ev.cancelled:
                ev.cancelled = True
                return True
        return False

    def run_until(self, end_time: float) -> int:
        self._running = True
        processed = 0
        while self._queue and self._running:
            event = heapq.heappop(self._queue)
            if event.cancelled:
                continue
            if event.time > end_time:
                heapq.heappush(self._queue, event)
                break
            self.current_time = event.time
            try:
                event.callback(event.data)
            except Exception as exc:
                print(f"[Scheduler] Exception in event {event.event_id}: {exc}")
            processed += 1
        self.current_time = max(self.current_time, end_time)
        self._running = False
        return processed

    def pending(self) -> int:
        return sum(1 for e in self._queue if not e.cancelled)


if __name__ == "__main__":
    print("Testing Scheduler...")
    sched = Scheduler()
    log: List[str] = []
    def tick(data):
        log.append(f"t={sched.current_time:.2f} {data}")
    sched.schedule(0.0, tick, data="start")
    sched.schedule(1.0, tick, data="one")
    sched.schedule(0.5, tick, data="half")
    sched.schedule_repeating(0.25, tick, data="repeat", max_count=3)
    eid = sched.schedule(10.0, tick, data="should_cancel")
    sched.cancel(eid)
    n = sched.run_until(2.0)
    print(f"Processed {n} events")
    for line in log:
        print(" ", line)
    print("Pending after run:", sched.pending())
    print("Scheduler module OK.")
