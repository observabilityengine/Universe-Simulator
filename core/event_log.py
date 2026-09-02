"""
Module 21 – Event Sourcing Log
Append-only event log with snapshots and replay.
Original, executable implementation.
"""

from __future__ import annotations
import json
import time
import hashlib
from typing import Any, Dict, List, Optional, Callable
from pathlib import Path


class EventLog:
    def __init__(self, path: Optional[str] = None):
        self.path = Path(path) if path else None
        self._events: List[Dict[str, Any]] = []
        self._snapshot: Optional[Dict[str, Any]] = None
        self._snapshot_index: int = -1

    def append(self, event_type: str, data: Dict[str, Any]) -> str:
        event = {
            "id": hashlib.sha256(f"{time.time()}{event_type}{data}".encode()).hexdigest()[:12],
            "ts": time.time(),
            "type": event_type,
            "data": data,
            "index": len(self._events),
        }
        self._events.append(event)
        if self.path:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")
        return event["id"]

    def take_snapshot(self, state: Dict[str, Any]) -> None:
        self._snapshot = dict(state)
        self._snapshot_index = len(self._events) - 1

    def replay(self, reducer: Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]], initial: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self._snapshot is not None:
            state = dict(self._snapshot)
            start = self._snapshot_index + 1
        else:
            state = dict(initial or {})
            start = 0
        for event in self._events[start:]:
            state = reducer(state, event)
        return state

    def get_events(self, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        if event_type is None:
            return list(self._events)
        return [e for e in self._events if e["type"] == event_type]


if __name__ == "__main__":
    print("Testing Event Log...")
    log = EventLog()
    log.append("created", {"name": "universe"})
    log.append("tick", {"n": 1})
    log.append("tick", {"n": 2})
    log.take_snapshot({"ticks": 2, "name": "universe"})
    log.append("tick", {"n": 3})
    def reducer(state, event):
        if event["type"] == "tick":
            state["ticks"] = state.get("ticks", 0) + 1
        elif event["type"] == "created":
            state["name"] = event["data"]["name"]
        return state
    final = log.replay(reducer)
    print("  Replayed state:", final)
    print("  Total events:", len(log.get_events()))
    print("Event Log module OK.")
