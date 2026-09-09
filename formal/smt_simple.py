"""Lightweight SMT fragment – linear integer arithmetic decision via bound propagation."""
from __future__ import annotations
from typing import Dict, List, Optional, Tuple

Constraint = Tuple[Dict[str, float], float, str]


def check_sat(constraints: List[Constraint], vars_: List[str]) -> Optional[Dict[str, float]]:
    lo = {v: float("-inf") for v in vars_}
    hi = {v: float("inf") for v in vars_}
    for _ in range(50):
        changed = False
        for coeffs, bound, op in constraints:
            for v in vars_:
                if v not in coeffs or abs(coeffs[v]) < 1e-12:
                    continue
                others = sum(
                    coeffs[u] * (0.0 if lo[u] == float("-inf") else (lo[u] if hi[u] == float("inf") else (lo[u] + hi[u]) / 2))
                    for u in coeffs if u != v
                )
                if abs(coeffs[v]) < 1e-12:
                    continue
                rhs = (bound - others) / coeffs[v]
                if op == "<=":
                    if coeffs[v] > 0:
                        if rhs < hi[v]:
                            hi[v] = rhs
                            changed = True
                    else:
                        if rhs > lo[v]:
                            lo[v] = rhs
                            changed = True
                elif op == ">=":
                    if coeffs[v] > 0:
                        if rhs > lo[v]:
                            lo[v] = rhs
                            changed = True
                    else:
                        if rhs < hi[v]:
                            hi[v] = rhs
                            changed = True
                elif op == "==":
                    lo[v] = hi[v] = rhs
                    changed = True
        if not changed:
            break
        for v in vars_:
            if lo[v] > hi[v] + 1e-9:
                return None
    sol = {}
    for v in vars_:
        if lo[v] == float("-inf") and hi[v] == float("inf"):
            sol[v] = 0.0
        elif lo[v] == float("-inf"):
            sol[v] = hi[v]
        elif hi[v] == float("inf"):
            sol[v] = lo[v]
        else:
            sol[v] = (lo[v] + hi[v]) / 2
    return sol


if __name__ == "__main__":
    c = [({"x": 1, "y": 1}, 5, "<="), ({"x": 1}, 1, ">="), ({"y": 1}, 1, ">=")]
    sol = check_sat(c, ["x", "y"])
    assert sol is not None and sol["x"] + sol["y"] <= 5.01
    print(f"smt_simple sol={sol}")
    print("smt_simple self-tests passed")
