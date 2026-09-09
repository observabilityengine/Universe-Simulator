"""LTL formula evaluation on finite traces."""
from __future__ import annotations
from typing import List, Set


def eval_atomic(trace: List[Set[str]], prop: str) -> List[bool]:
    return [prop in labels for labels in trace]


def eval_not(vals: List[bool]) -> List[bool]:
    return [not v for v in vals]


def eval_and(a: List[bool], b: List[bool]) -> List[bool]:
    return [x and y for x, y in zip(a, b)]


def eval_x(vals: List[bool]) -> List[bool]:
    return vals[1:] + [False]


def eval_f(vals: List[bool]) -> List[bool]:
    n = len(vals)
    out = [False] * n
    seen = False
    for i in range(n - 1, -1, -1):
        seen = seen or vals[i]
        out[i] = seen
    return out


def eval_g(vals: List[bool]) -> List[bool]:
    n = len(vals)
    out = [False] * n
    ok = True
    for i in range(n - 1, -1, -1):
        ok = ok and vals[i]
        out[i] = ok
    return out


def eval_u(a: List[bool], b: List[bool]) -> List[bool]:
    n = len(a)
    out = [False] * n
    for i in range(n):
        for j in range(i, n):
            if b[j] and all(a[k] for k in range(i, j)):
                out[i] = True
                break
    return out


if __name__ == "__main__":
    trace = [{"p"}, {"p", "q"}, {"q"}, set()]
    p = eval_atomic(trace, "p")
    f_p = eval_f(p)
    assert f_p[0] is True
    g_p = eval_g(p)
    assert g_p[0] is False
    print(f"temporal_logic F(p)={f_p}")
    print("temporal_logic self-tests passed")
