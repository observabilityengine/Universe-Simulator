"""Quantum circuit composition and simulation."""
from __future__ import annotations
from typing import List, Tuple
from .qubit import QubitState
from .gates import apply_single, apply_cnot, H, X, Z, S, T


class QuantumCircuit:
    def __init__(self, n_qubits: int):
        self.n = n_qubits
        self.ops: List[Tuple] = []

    def h(self, q: int) -> "QuantumCircuit":
        self.ops.append(("H", q))
        return self

    def x(self, q: int) -> "QuantumCircuit":
        self.ops.append(("X", q))
        return self

    def z(self, q: int) -> "QuantumCircuit":
        self.ops.append(("Z", q))
        return self

    def cnot(self, c: int, t: int) -> "QuantumCircuit":
        self.ops.append(("CNOT", c, t))
        return self

    def run(self, seed: int = 42) -> QubitState:
        state = QubitState(self.n, seed=seed)
        gate_map = {"H": H, "X": X, "Z": Z, "S": S, "T": T}
        for op in self.ops:
            if op[0] == "CNOT":
                apply_cnot(state, op[1], op[2])
            else:
                apply_single(state, gate_map[op[0]], op[1])
        return state


if __name__ == "__main__":
    qc = QuantumCircuit(2).h(0).cnot(0, 1)
    st = qc.run()
    probs = st.probabilities()
    assert abs(probs[0] - 0.5) < 1e-5 and abs(probs[3] - 0.5) < 1e-5
    print(f"circuit Bell probs={probs}")
    print("circuit self-tests passed")
