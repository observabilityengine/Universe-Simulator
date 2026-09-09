"""CTL model checker for finite-state transition systems (EF, AG operators)."""
from __future__ import annotations
from typing import Dict, List, Set


class TransitionSystem:
    def __init__(self, states: List[str], init: str, transitions: Dict[str, List[str]], labels: Dict[str, Set[str]]):
        self.states = states
        self.init = init
        self.trans = transitions
        self.labels = labels


def sat_atomic(ts: TransitionSystem, prop: str) -> Set[str]:
    return {s for s in ts.states if prop in ts.labels.get(s, set())}


def sat_ef(ts: TransitionSystem, phi_states: Set[str]) -> Set[str]:
    result = set(phi_states)
    changed = True
    while changed:
        changed = False
        for s in ts.states:
            if s not in result and any(n in result for n in ts.trans.get(s, [])):
                result.add(s)
                changed = True
    return result


def sat_ag(ts: TransitionSystem, phi_states: Set[str]) -> Set[str]:
    result = set(phi_states)
    changed = True
    while changed:
        changed = False
        for s in list(result):
            if not all(n in result for n in ts.trans.get(s, [])):
                result.discard(s)
                changed = True
    return result


def check_ef(ts: TransitionSystem, prop: str) -> bool:
    target = sat_atomic(ts, prop)
    reachable = sat_ef(ts, target)
    return ts.init in reachable


if __name__ == "__main__":
    ts = TransitionSystem(
        states=["s0", "s1", "s2"],
        init="s0",
        transitions={"s0": ["s1"], "s1": ["s2"], "s2": ["s2"]},
        labels={"s0": set(), "s1": set(), "s2": {"goal"}},
    )
    assert check_ef(ts, "goal")
    print("model_checker EF goal reachable")
    print("model_checker self-tests passed")
