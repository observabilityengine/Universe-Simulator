"""Variational Quantum Eigensolver – optimise ansatz for Hamiltonian expectation."""
from __future__ import annotations
import math
import random
from typing import Callable, Tuple
from .qubit import QubitState
from .gates import apply_single, H


def pauli_z_expectation(state: QubitState, qubit: int = 0) -> float:
    return state.expectation_z(qubit)


def simple_ansatz(theta: float, n: int = 1) -> QubitState:
    s = QubitState(n)
    apply_single(s, H, 0)
    for i in range(s.dim):
        if i & 1:
            s.amps[i] *= complex(math.cos(theta), math.sin(theta))
    s.normalize()
    apply_single(s, H, 0)
    return s


def vqe_minimize(hamiltonian: Callable[[QubitState], float], n_steps: int = 30, lr: float = 0.3, seed: int = 42) -> Tuple[float, float]:
    rng = random.Random(seed)
    theta = rng.uniform(0, math.pi)
    best_energy = float("inf")
    best_theta = theta
    for _ in range(n_steps):
        e_plus = hamiltonian(simple_ansatz(theta + 0.01))
        e_minus = hamiltonian(simple_ansatz(theta - 0.01))
        grad = (e_plus - e_minus) / 0.02
        theta -= lr * grad
        energy = hamiltonian(simple_ansatz(theta))
        if energy < best_energy:
            best_energy = energy
            best_theta = theta
    return best_theta, best_energy


if __name__ == "__main__":
    def H_z(state):
        return pauli_z_expectation(state, 0)
    theta, energy = vqe_minimize(H_z, n_steps=40, lr=0.5)
    assert energy < 0
    print(f"vqe theta={theta:.3f} energy={energy:.3f}")
    print("vqe self-tests passed")
