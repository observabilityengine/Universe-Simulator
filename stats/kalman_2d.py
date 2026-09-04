"""
Universe Simulator - 2-D Constant Velocity Kalman Filter
Original tracking filter for position + velocity.
"""

from __future__ import annotations

from typing import List, Tuple

class Kalman2D:
    def __init__(self, dt: float = 1.0, process_var: float = 0.1, meas_var: float = 1.0):
        self.dt = dt
        self.x = [0.0, 0.0, 0.0, 0.0]  # px, py, vx, vy
        self.P = [[100.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
        self.Q = [[process_var if i == j else 0.0 for j in range(4)] for i in range(4)]
        self.R = [[meas_var, 0.0], [0.0, meas_var]]

    def predict(self) -> None:
        dt = self.dt
        F = [
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
        new_x = [sum(F[i][j] * self.x[j] for j in range(4)) for i in range(4)]
        new_P = [[0.0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_P[i][j] = sum(F[i][k] * self.P[k][j] for k in range(4))
        for i in range(4):
            for j in range(4):
                self.P[i][j] = sum(new_P[i][k] * F[j][k] for k in range(4)) + self.Q[i][j]
        self.x = new_x

    def update(self, zx: float, zy: float) -> None:
        H = [[1, 0, 0, 0], [0, 1, 0, 0]]
        y = [zx - self.x[0], zy - self.x[1]]
        S = [[0.0, 0.0], [0.0, 0.0]]
        for i in range(2):
            for j in range(2):
                S[i][j] = sum(H[i][k] * self.P[k][j] for k in range(4)) + self.R[i][j]
        # inverse 2x2
        det = S[0][0]*S[1][1] - S[0][1]*S[1][0]
        invS = [[S[1][1]/det, -S[0][1]/det], [-S[1][0]/det, S[0][0]/det]]
        K = [[0.0]*2 for _ in range(4)]
        for i in range(4):
            for j in range(2):
                K[i][j] = sum(self.P[i][k] * H[j][k] for k in range(4))
        K2 = [[sum(K[i][k] * invS[k][j] for k in range(2)) for j in range(2)] for i in range(4)]
        for i in range(4):
            self.x[i] += K2[i][0]*y[0] + K2[i][1]*y[1]
        IKH = [[(1 if i==j else 0) - sum(K2[i][k]*H[k][j] for k in range(2)) for j in range(4)] for i in range(4)]
        new_P = [[sum(IKH[i][k]*self.P[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
        self.P = new_P

    def position(self) -> Tuple[float, float]:
        return self.x[0], self.x[1]

if __name__ == "__main__":
    kf = Kalman2D()
    for i in range(10):
        kf.predict()
        kf.update(i * 1.0 + 0.1, i * 0.5)
    px, py = kf.position()
    assert abs(px - 9.0) < 2.0
    print("kalman_2d self-test passed", px, py)
