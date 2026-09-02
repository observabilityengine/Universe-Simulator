"""
Module 16 – FFT Filter
Low-pass / high-pass / band-pass filtering via real FFT.
Original, executable implementation.
"""

from __future__ import annotations
import numpy as np
from typing import Tuple


def lowpass(signal: np.ndarray, cutoff: float, fs: float) -> np.ndarray:
    n = len(signal)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    spectrum = np.fft.rfft(signal)
    spectrum[freqs > cutoff] = 0.0
    return np.fft.irfft(spectrum, n=n)


def highpass(signal: np.ndarray, cutoff: float, fs: float) -> np.ndarray:
    n = len(signal)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    spectrum = np.fft.rfft(signal)
    spectrum[freqs < cutoff] = 0.0
    return np.fft.irfft(spectrum, n=n)


def bandpass(signal: np.ndarray, low: float, high: float, fs: float) -> np.ndarray:
    n = len(signal)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    spectrum = np.fft.rfft(signal)
    spectrum[(freqs < low) | (freqs > high)] = 0.0
    return np.fft.irfft(spectrum, n=n)


def power_spectrum(signal: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray]:
    n = len(signal)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    spectrum = np.fft.rfft(signal)
    power = (np.abs(spectrum) ** 2) / n
    return freqs, power


if __name__ == "__main__":
    print("Testing FFT Filter...")
    fs = 500.0
    t = np.arange(0, 1.0, 1.0 / fs)
    clean = np.sin(2 * np.pi * 5 * t)
    noisy = clean + 0.5 * np.sin(2 * np.pi * 50 * t)
    filtered = lowpass(noisy, cutoff=10.0, fs=fs)
    mse = np.mean((filtered - clean) ** 2)
    print(f"  MSE after low-pass: {mse:.6f}")
    freqs, pwr = power_spectrum(noisy, fs)
    peak = freqs[np.argmax(pwr[1:]) + 1]
    print(f"  Dominant frequency in noisy signal: {peak:.1f} Hz")
    print("FFT Filter module OK.")
