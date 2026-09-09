"""Particle-Mesh gravity via FFT Poisson solver on a periodic grid."""
from __future__ import annotations
import cmath
import math
from typing import List

Vec = List[float]


def _fft1d(a: List[complex], inverse: bool = False) -> List[complex]:
    n = len(a)
    if n == 1:
        return a
    if n & (n - 1):
        n2 = 1
        while n2 < n:
            n2 <<= 1
        a = a + [0j] * (n2 - n)
        n = n2
    even = _fft1d(a[0::2], inverse)
    odd = _fft1d(a[1::2], inverse)
    out = [0j] * n
    sign = 1 if inverse else -1
    for k in range(n // 2):
        w = cmath.exp(sign * 2j * math.pi * k / n) * odd[k]
        out[k] = even[k] + w
        out[k + n // 2] = even[k] - w
    if inverse:
        out = [x / 2 for x in out]
    return out


def fft2d(grid: List[List[complex]], inverse: bool = False) -> List[List[complex]]:
    n = len(grid)
    rows = [_fft1d(row[:], inverse) for row in grid]
    for j in range(n):
        col = [rows[i][j] for i in range(n)]
        col = _fft1d(col, inverse)
        for i in range(n):
            rows[i][j] = col[i]
    return rows


def deposit_cic(positions: List[Vec], masses: List[float], n_grid: int, box_size: float) -> List[List[float]]:
    dens = [[0.0] * n_grid for _ in range(n_grid)]
    cell = box_size / n_grid
    for p, m in zip(positions, masses):
        x = (p[0] % box_size) / cell
        y = (p[1] % box_size) / cell
        i0, j0 = int(x) % n_grid, int(y) % n_grid
        i1, j1 = (i0 + 1) % n_grid, (j0 + 1) % n_grid
        dx, dy = x - int(x), y - int(y)
        dens[j0][i0] += m * (1 - dx) * (1 - dy)
        dens[j0][i1] += m * dx * (1 - dy)
        dens[j1][i0] += m * (1 - dx) * dy
        dens[j1][i1] += m * dx * dy
    mean = sum(sum(row) for row in dens) / (n_grid * n_grid)
    for j in range(n_grid):
        for i in range(n_grid):
            dens[j][i] -= mean
    return dens


def solve_poisson_fft(density: List[List[float]], box_size: float, G: float = 1.0) -> List[List[float]]:
    n = len(density)
    grid = [[complex(density[j][i]) for i in range(n)] for j in range(n)]
    hat = fft2d(grid, inverse=False)
    for j in range(n):
        ky = (j if j <= n // 2 else j - n) * 2 * math.pi / box_size
        for i in range(n):
            kx = (i if i <= n // 2 else i - n) * 2 * math.pi / box_size
            k2 = kx * kx + ky * ky
            if k2 < 1e-30:
                hat[j][i] = 0j
            else:
                hat[j][i] *= -4 * math.pi * G / k2
    phi_c = fft2d(hat, inverse=True)
    inv = 1.0 / (n * n)
    return [[phi_c[j][i].real * inv for i in range(n)] for j in range(n)]


def pm_accelerations(positions: List[Vec], masses: List[float], n_grid: int = 32, box_size: float = 1.0, G: float = 1.0) -> List[Vec]:
    dens = deposit_cic(positions, masses, n_grid, box_size)
    phi = solve_poisson_fft(dens, box_size, G)
    cell = box_size / n_grid
    acc = []
    for p in positions:
        x = (p[0] % box_size) / cell
        y = (p[1] % box_size) / cell
        i0, j0 = int(x) % n_grid, int(y) % n_grid
        ip, im = (i0 + 1) % n_grid, (i0 - 1) % n_grid
        jp, jm = (j0 + 1) % n_grid, (j0 - 1) % n_grid
        ax = -(phi[j0][ip] - phi[j0][im]) / (2 * cell)
        ay = -(phi[jp][i0] - phi[jm][i0]) / (2 * cell)
        acc.append([ax, ay])
    return acc


if __name__ == "__main__":
    pos = [[0.3, 0.5], [0.7, 0.5]]
    masses = [1.0, 1.0]
    acc = pm_accelerations(pos, masses, n_grid=16, box_size=1.0)
    assert len(acc) == 2 and len(acc[0]) == 2
    print(f"particle_mesh acc={acc}")
    print("particle_mesh self-tests passed")
