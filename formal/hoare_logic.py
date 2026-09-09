"""Hoare triple checker for a tiny imperative language."""
from __future__ import annotations
from typing import Callable, Dict

State = Dict[str, int]
Pred = Callable[[State], bool]


def wp_assign(var: str, expr: Callable[[State], int], post: Pred) -> Pred:
    def pre(s: State) -> bool:
        s2 = dict(s)
        s2[var] = expr(s)
        return post(s2)
    return pre


def check_triple(pre: Pred, wp_prog: Callable[[Pred], Pred], post: Pred, tests: list) -> bool:
    derived = wp_prog(post)
    return all(not pre(s) or derived(s) for s in tests)


if __name__ == "__main__":
    post = lambda s: s["x"] > 1
    wp = lambda p: wp_assign("x", lambda s: s["x"] + 1, p)
    pre = lambda s: s["x"] > 0
    tests = [{"x": 1}, {"x": 5}, {"x": 0}]
    assert check_triple(pre, wp, post, tests)
    print("hoare_logic triple holds")
    print("hoare_logic self-tests passed")
