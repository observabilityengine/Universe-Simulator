"""
Module 75 – DPLL SAT Solver
Complete CDCL-lite DPLL solver for CNF formulas.
"""

from __future__ import annotations
from typing import List, Dict, Optional, Set

Literal = int
Clause = List[Literal]
CNF = List[Clause]


def _unit_propagate(clauses: CNF, assignment: Dict[int, bool]) -> Optional[CNF]:
    changed = True
    while changed:
        changed = False
        new_clauses = []
        for clause in clauses:
            new_clause = []
            satisfied = False
            for lit in clause:
                var = abs(lit)
                if var in assignment:
                    val = assignment[var]
                    if (lit > 0 and val) or (lit < 0 and not val):
                        satisfied = True
                        break
                else:
                    new_clause.append(lit)
            if satisfied:
                continue
            if not new_clause:
                return None
            if len(new_clause) == 1:
                lit = new_clause[0]
                var = abs(lit)
                val = lit > 0
                if var in assignment and assignment[var] != val:
                    return None
                if var not in assignment:
                    assignment[var] = val
                    changed = True
            new_clauses.append(new_clause)
        clauses = new_clauses
    return clauses


def dpll(clauses: CNF, assignment: Optional[Dict[int, bool]] = None) -> Optional[Dict[int, bool]]:
    if assignment is None:
        assignment = {}
    clauses = _unit_propagate(clauses, assignment)
    if clauses is None:
        return None
    if not clauses:
        return dict(assignment)
    vars_in_clauses: Set[int] = set()
    for c in clauses:
        for lit in c:
            vars_in_clauses.add(abs(lit))
    unassigned = [v for v in vars_in_clauses if v not in assignment]
    if not unassigned:
        return dict(assignment)
    var = unassigned[0]
    for val in [True, False]:
        new_assign = dict(assignment)
        new_assign[var] = val
        result = dpll(clauses, new_assign)
        if result is not None:
            return result
    return None


if __name__ == "__main__":
    print("Testing SAT Solver...")
    formula = [[1, -2], [-1, 2], [-1, -2]]
    sol = dpll(formula)
    print(f"  Solution: {sol}")
    unsat = [[1], [-1]]
    print(f"  UNSAT result: {dpll(unsat)}")
    print("SAT Solver module OK.")
