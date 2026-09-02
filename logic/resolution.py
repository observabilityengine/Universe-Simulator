"""
Universe Simulator - Propositional Resolution
Original resolution refutation for CNF clauses.
"""

from __future__ import annotations

from typing import FrozenSet, List, Set, Tuple

Literal = str  # "P" or "~P"
Clause = FrozenSet[Literal]


def negate(lit: Literal) -> Literal:
    return lit[1:] if lit.startswith("~") else "~" + lit


def resolve(c1: Clause, c2: Clause) -> Set[Clause]:
    resolvents = set()
    for lit in c1:
        if negate(lit) in c2:
            new = (c1 - {lit}) | (c2 - {negate(lit)})
            resolvents.add(frozenset(new))
    return resolvents


def resolution_refute(clauses: List[Clause]) -> bool:
    """Return True if unsatisfiable (empty clause derived)."""
    s: Set[Clause] = set(clauses)
    while True:
        new = set()
        pairs = [(a, b) for i, a in enumerate(s) for b in list(s)[i+1:]]
        for c1, c2 in pairs:
            for r in resolve(c1, c2):
                if not r:
                    return True  # empty clause
                if r not in s:
                    new.add(r)
        if not new:
            return False
        s |= new


if __name__ == "__main__":
    # P, ~P  -> unsat
    assert resolution_refute([frozenset(["P"]), frozenset(["~P"])])
    # P v Q, ~P, ~Q -> unsat
    assert resolution_refute([frozenset(["P", "Q"]), frozenset(["~P"]), frozenset(["~Q"])])
    # P  -> sat
    assert not resolution_refute([frozenset(["P"])])
    print("resolution self-test passed")
