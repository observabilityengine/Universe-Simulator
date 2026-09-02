"""
Universe Simulator - Synchronous Event Bus
Original pub/sub for internal observability events.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, DefaultDict, List


class EventBus:
    def __init__(self) -> None:
        self._subs: DefaultDict[str, List[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, event: str, handler: Callable[[Any], None]) -> None:
        self._subs[event].append(handler)

    def unsubscribe(self, event: str, handler: Callable[[Any], None]) -> None:
        if handler in self._subs[event]:
            self._subs[event].remove(handler)

    def publish(self, event: str, payload: Any = None) -> None:
        for h in list(self._subs[event]):
            h(payload)

    def clear(self) -> None:
        self._subs.clear()


if __name__ == "__main__":
    bus = EventBus()
    received = []
    bus.subscribe("tick", lambda p: received.append(p))
    bus.publish("tick", 42)
    bus.publish("tick", 99)
    assert received == [42, 99]
    print("event_bus self-test passed")
