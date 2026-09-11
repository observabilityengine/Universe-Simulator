"""Hilbert transform via FFT (analytic signal)."""
from __future__ import annotations
import cmath
import math
from typing import List, Tuple
from .fft import fft, ifft


def hilbert(x: List[float]) -> List[complex]:
    """Return analytic signal z = x + j * Hilbert(x)."""
    n = len(x)
    X = fft(x)
    # Pad length may exceed n
    N = len(X)
    h = [0.0] * N
    if N % 2 == 0:
        h[0] = h[N // 2] = 1.0
        for i in range(1, N // 2):
            h[i] = 2.0
    else:
        h[0] = 1.0
        for i in range(1, (N + 1) // 2):
            h[i] = 2.0
    filtered = [X[i] * h[i] for i in range(N)]
    # ifft returns real; reconstruct complex via separate imag path
    # Use manual inverse for complex
    y = _ifft_complex(filtered)
    return y[:n]


def _ifft_complex(X: List[complex]) -> List[complex]:
    n = len(X)
    conjugated = [z.conjugate() for z in X]
    # reuse real fft machinery on conjugated
    from .fft import _fft
    y = _fft(conjugated)
    return [z.conjugate() / n for z in y]


def envelope(x: List[float]) -> List[float]:
    z = hilbert(x)
    return [abs(c) for c in z]


if __name__ == "__main__":
    x = [math.sin(2 * math.pi * 5 * i / 64) for i in range(64)]
    env = envelope(x)
    assert abs(sum(env) / len(env) - 1.0) < 0.3
    print(f"hilbert mean_env={sum(env)/len(env):.3f}")
    print("hilbert self-tests passed")
