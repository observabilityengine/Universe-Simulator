"""
Module 14 – Kalman Filter
1-D and multi-dimensional linear Kalman filter.
Original, executable implementation.
"""

from __future__ import annotations
import numpy as np
from typing import Optional


class KalmanFilter1D:
    def __init__(self, process_variance: float, measurement_variance: float, initial_estimate: float = 0.0, initial_error: float = 1.0):
        self.q = process_variance
        self.r = measurement_variance
        self.x = initial_estimate
        self.p = initial_error

    def update(self, measurement: float) -> float:
        self.p = self.p + self.q
        k = self.p / (self.p + self.r)
        self.x = self.x + k * (measurement - self.x)
        self.p = (1.0 - k) * self.p
        return self.x


class KalmanFilter:
    def __init__(self, F: np.ndarray, H: np.ndarray, Q: np.ndarray, R: np.ndarray, x0: np.ndarray, P0: np.ndarray):
        self.F = np.asarray(F, dtype=float)
        self.H = np.asarray(H, dtype=float)
        self.Q = np.asarray(Q, dtype=float)
        self.R = np.asarray(R, dtype=float)
        self.x = np.asarray(x0, dtype=float).reshape(-1, 1)
        self.P = np.asarray(P0, dtype=float)

    def predict(self) -> np.ndarray:
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.x.flatten()

    def update(self, z: np.ndarray) -> np.ndarray:
        z = np.asarray(z, dtype=float).reshape(-1, 1)
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        I = np.eye(self.P.shape[0])
        self.P = (I - K @ self.H) @ self.P
        return self.x.flatten()

    def step(self, z: np.ndarray) -> np.ndarray:
        self.predict()
        return self.update(z)


if __name__ == "__main__":
    print("Testing Kalman Filter...")
    kf1 = KalmanFilter1D(process_variance=1e-5, measurement_variance=0.1**2)
    true = 42.0
    estimates = []
    for i in range(30):
        z = true + np.random.normal(0, 0.1)
        est = kf1.update(z)
        estimates.append(est)
    print(f"  1-D final estimate: {estimates[-1]:.4f} (true={true})")
    dt = 0.1
    F = np.array([[1, dt], [0, 1]])
    H = np.array([[1.0, 0.0]])
    Q = np.array([[0.01, 0], [0, 0.01]])
    R = np.array([[0.1]])
    kf = KalmanFilter(F, H, Q, R, x0=[0, 1], P0=np.eye(2))
    for i in range(20):
        z = [i * dt * 1.0 + np.random.normal(0, 0.3)]
        kf.step(z)
    print(f"  2-D position estimate: {kf.x[0,0]:.3f}")
    print("Kalman Filter module OK.")
