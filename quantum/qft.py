"""Quantum Fourier Transform on n qubits."""
from __future__ import annotations
import cmath
import math
from .qubit import QubitState
from .gates import apply_single, H


def controlled_phase(state: QubitState, control: int, target: int, k: int) -> None:
    angle = 2 * math.pi / (1 << k)
    phase = cmath.exp(1j * angle)
    for i in range(state.dim):
        if ((i >> control) & 1) and ((i >> target) & 1):
            state.amps[i] *= phase
    state.normalize()


def qft(state: QubitState) -> None:
    n = state.n
    for j in range(n):
        apply_single(state, H, j)
        for k in range(2, n - j + 1):
            controlled_phase(state, j + k - 1, j, k)
    for i in range(n // 2):
        a, b = i, n - 1 - i
        new = [0j] * state.dim
        for idx in range(state.dim):
            bit_a = (idx >> a) & 1
            bit_b = (idx >> b) & 1
            new_idx = idx
            if bit_a != bit_b:
                new_idx ^= (1 << a) | (1 << b)
            new[new_idx] = state.amps[idx]
        state.amps = new


if __name__ == "__main__":
    from .gates import apply_single, X
    s = QubitState(2)
    apply_single(s, X, 0)
    qft(s)
    mags = [abs(a) for a in s.amps]
    assert all(abs(m - mags[0]) < 1e-5 for m in mags)
    print(f"qft magnitudes={mags}")
    print("qft self-tests passed")
