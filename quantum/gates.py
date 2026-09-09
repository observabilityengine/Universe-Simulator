"""Quantum gates as unitary matrices applied to state vectors."""
from __future__ import annotations
import cmath
import math
from typing import List
from .qubit import QubitState


def apply_single(state: QubitState, gate: List[List[complex]], target: int) -> None:
    seen = set()
    result = [0j] * state.dim
    for i in range(state.dim):
        i0 = i & ~(1 << target)
        if i0 in seen:
            continue
        seen.add(i0)
        i1 = i0 | (1 << target)
        a0, a1 = state.amps[i0], state.amps[i1]
        result[i0] = gate[0][0] * a0 + gate[0][1] * a1
        result[i1] = gate[1][0] * a0 + gate[1][1] * a1
    state.amps = result
    state.normalize()


H = [[1 / math.sqrt(2), 1 / math.sqrt(2)], [1 / math.sqrt(2), -1 / math.sqrt(2)]]
X = [[0, 1], [1, 0]]
Z = [[1, 0], [0, -1]]
S = [[1, 0], [0, 1j]]
T = [[1, 0], [0, cmath.exp(1j * math.pi / 4)]]


def apply_cnot(state: QubitState, control: int, target: int) -> None:
    new = state.amps[:]
    for i in range(state.dim):
        if (i >> control) & 1:
            j = i ^ (1 << target)
            if i < j:
                new[i], new[j] = state.amps[j], state.amps[i]
    state.amps = new


if __name__ == "__main__":
    s = QubitState(1)
    apply_single(s, H, 0)
    probs = s.probabilities()
    assert abs(probs[0] - 0.5) < 1e-6 and abs(probs[1] - 0.5) < 1e-6
    print(f"gates H|0> probs={probs}")
    print("gates self-tests passed")
