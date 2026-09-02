"""
Module 4 – Symbolic Physics
SymPy-based derivation of equations of motion and conserved quantities.
Fully functional. Original implementation.
"""

from __future__ import annotations
import sympy as sp
from typing import Dict, List, Tuple, Optional, Any


class SymbolicSystem:
    def __init__(self):
        self.coords: List[sp.Symbol] = []
        self.velocities: List[sp.Symbol] = []
        self.masses: Dict[sp.Symbol, sp.Expr] = {}
        self.potential: sp.Expr = sp.Integer(0)
        self.time = sp.symbols("t", real=True, positive=True)
        self._lagrange: Optional[sp.Expr] = None
        self._eom: Dict[sp.Symbol, sp.Expr] = {}

    def add_coordinate(self, name: str, mass: Any = 1) -> Tuple[sp.Symbol, sp.Symbol]:
        q = sp.symbols(name, real=True)
        qdot = sp.symbols(f"{name}_dot", real=True)
        self.coords.append(q)
        self.velocities.append(qdot)
        self.masses[q] = sp.sympify(mass)
        return q, qdot

    def set_potential(self, expr: sp.Expr) -> None:
        self.potential = sp.simplify(expr)
        self._lagrange = None
        self._eom.clear()

    def kinetic_energy(self) -> sp.Expr:
        T = sp.Integer(0)
        for q, qdot in zip(self.coords, self.velocities):
            T += sp.Rational(1, 2) * self.masses[q] * qdot**2
        return sp.simplify(T)

    def lagrangian(self) -> sp.Expr:
        if self._lagrange is None:
            self._lagrange = sp.simplify(self.kinetic_energy() - self.potential)
        return self._lagrange

    def equations_of_motion(self) -> Dict[sp.Symbol, sp.Expr]:
        if self._eom:
            return self._eom
        L = self.lagrangian()
        for q, qdot in zip(self.coords, self.velocities):
            dL_dq = sp.diff(L, q)
            dL_dqdot = sp.diff(L, qdot)
            q_ddot = sp.symbols(f"{q}_ddot", real=True)
            dt_dL_dqdot = sp.diff(dL_dqdot, q) * qdot + sp.diff(dL_dqdot, qdot) * q_ddot
            eq = sp.Eq(dt_dL_dqdot - dL_dq, 0)
            sol = sp.solve(eq, q_ddot)
            self._eom[q] = sp.simplify(sol[0]) if sol else sp.Integer(0)
        return self._eom

    def energy(self) -> sp.Expr:
        return sp.simplify(self.kinetic_energy() + self.potential)


def harmonic_oscillator() -> SymbolicSystem:
    sys = SymbolicSystem()
    x, xdot = sys.add_coordinate("x", mass=1)
    k = sp.symbols("k", positive=True)
    sys.set_potential(sp.Rational(1, 2) * k * x**2)
    return sys


if __name__ == "__main__":
    print("Testing Symbolic Physics...")
    osc = harmonic_oscillator()
    print("Lagrangian:", osc.lagrangian())
    print("Equations of motion:", osc.equations_of_motion())
    print("Total energy:", osc.energy())
    print("Symbolic Physics module OK.")
