"""
Module 19 – Finite State Machine Engine
Deterministic FSM with guards and actions.
Original, executable implementation.
"""

from __future__ import annotations
from typing import Any, Callable, Dict, Optional, Hashable


class StateMachine:
    def __init__(self, initial: Hashable):
        self.state = initial
        self._transitions: Dict[Hashable, Dict[Hashable, tuple]] = {}
        self.history: list = [initial]

    def add_transition(self, source: Hashable, event: Hashable, target: Hashable, guard: Optional[Callable[[], bool]] = None, action: Optional[Callable[[], None]] = None) -> None:
        if source not in self._transitions:
            self._transitions[source] = {}
        self._transitions[source][event] = (target, guard, action)

    def trigger(self, event: Hashable) -> bool:
        table = self._transitions.get(self.state, {})
        if event not in table:
            return False
        target, guard, action = table[event]
        if guard is not None and not guard():
            return False
        if action is not None:
            action()
        self.state = target
        self.history.append(target)
        return True


if __name__ == "__main__":
    print("Testing Finite State Machine...")
    door = StateMachine("closed")
    locked = {"value": False}
    door.add_transition("closed", "open", "open", guard=lambda: not locked["value"])
    door.add_transition("open", "close", "closed")
    door.add_transition("closed", "lock", "closed", action=lambda: locked.update({"value": True}))
    door.add_transition("closed", "unlock", "closed", action=lambda: locked.update({"value": False}))
    print("  start:", door.state)
    print("  open ->", door.trigger("open"), "state=", door.state)
    print("  close ->", door.trigger("close"), "state=", door.state)
    print("  lock ->", door.trigger("lock"))
    print("  open (should fail) ->", door.trigger("open"), "state=", door.state)
    print("  unlock ->", door.trigger("unlock"))
    print("  open ->", door.trigger("open"), "state=", door.state)
    print("FSM module OK.")
