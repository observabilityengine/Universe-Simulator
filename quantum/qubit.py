"""Single-qubit and multi-qubit state vectors with measurement."""
from __future__ import annotations
import cmath
import math
import random
from typing import List, Tuple


class QubitState:
    def __init__(self, n_qubits: int = 1, seed: int = 42):
        self.n = n_qubits
        self.dim = 1 << n_qubits
        self.amps: List[complex] = [0j] * self.dim
        self.amps[0] = 1.0 + 0j
        self.rng = random.Random(seed)

    def normalize(self) -> None:
        nrm = math.sqrt(sum(abs(a) ** 2 for a in self.amps))
        if nrm > 1e-15:
            self.amps = [a / nrm for a in self.amps]

    def probabilities(self) -> List[float]:
        return [abs(a) ** 2 for a in self.amps]

    def measure(self) -> int:
        probs = self.probabilities()
        r = self.rng.random()
        cum = 0.0
        for i, p in enumerate(probs):
            cum += p
            if r <= cum:
                self.amps = [0j] * self.dim
                self.amps[i] = 1.0 + 0j
                return i
        return self.dim - 1

    def expectation_z(self, qubit: int = 0) -> float:
        exp = 0.0
        for i, a in enumerate(self.amps):
            bit = (i >> qubit) & 1
            sign = 1 if bit == 0 else -1
            exp += sign * abs(a) ** 2
        return exp


if __name__ == "__main__":
    q = QubitState(2)
    assert abs(q.probabilities()[0] - 1.0) < 1e-9
    assert abs(q.expectation_z(0) - 1.0) < 1e-9
    print(f"qubit |00\u27e9 probs={q.probabilities()}")
    print("qubit self-tests passed")
