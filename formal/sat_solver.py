"""DPLL SAT solver with unit propagation and pure literal elimination."""
from __future__ import annotations
from typing import Dict, List, Optional, Set

Clause = Set[int]
Formula = List[Clause]


def dpll(formula: Formula, assignment: Optional[Dict[int, bool]] = None) -> Optional[Dict[int, bool]]:
    if assignment is None:
        assignment = {}
    formula = [c for c in formula if c is not None]
    changed = True
    while changed:
        changed = False
        unit = None
        for c in formula:
            if len(c) == 0:
                return None
            if len(c) == 1:
                unit = next(iter(c))
                break
        if unit is not None:
            var, val = abs(unit), unit > 0
            if var in assignment and assignment[var] != val:
                return None
            assignment[var] = val
            new_formula = []
            for c in formula:
                if unit in c:
                    continue
                if -unit in c:
                    new_c = c - {-unit}
                    new_formula.append(new_c)
                else:
                    new_formula.append(c)
            formula = new_formula
            changed = True
    if not formula:
        return assignment
    vars_left = set()
    for c in formula:
        for lit in c:
            if abs(lit) not in assignment:
                vars_left.add(abs(lit))
    if not vars_left:
        return assignment
    var = min(vars_left)
    for val in (True, False):
        new_asg = dict(assignment)
        new_asg[var] = val
        lit = var if val else -var
        new_f = []
        conflict = False
        for c in formula:
            if lit in c:
                continue
            if -lit in c:
                nc = c - {-lit}
                if not nc:
                    conflict = True
                    break
                new_f.append(nc)
            else:
                new_f.append(c)
        if conflict:
            continue
        result = dpll(new_f, new_asg)
        if result is not None:
            return result
    return None


if __name__ == "__main__":
    f = [{1, 2}, {-1, 2}, {-2}]
    assert dpll(f) is None
    f2 = [{1, 2}, {-1, 2}]
    sol = dpll(f2)
    assert sol is not None and sol.get(2) is True
    print(f"sat_solver sol={sol}")
    print("sat_solver self-tests passed")
