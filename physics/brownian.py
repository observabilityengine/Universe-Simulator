"""Standard Brownian motion (Wiener process) path simulation.

Complexity: O(steps).
Returns time grid and positions. Supports multi-dimensional independent paths.
Original implementation.
"""
from __future__ import annotations

import numpy as np
from typing import Tuple


def brownian_motion(
    t_final: float,
    steps: int,
    dim: int = 1,
    x0: float | np.ndarray = 0.0,
    seed: int | None = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Simulate Brownian motion on [0, t_final].

    Returns (times, path) with path shape (steps+1, dim).
    """
    if steps < 1 or t_final <= 0:
        raise ValueError("steps >= 1 and t_final > 0 required")
    rng = np.random.default_rng(seed)
    dt = t_final / steps
    times = np.linspace(0.0, t_final, steps + 1)
    increments = rng.normal(0.0, np.sqrt(dt), size=(steps, dim))
    path = np.zeros((steps + 1, dim))
    path[0] = np.broadcast_to(np.asarray(x0, dtype=float), (dim,))
    path[1:] = path[0] + np.cumsum(increments, axis=0)
    return times, path


if __name__ == "__main__":
    t, x = brownian_motion(1.0, 100, dim=1, seed=42)
    assert t.shape == (101,)
    assert x.shape == (101, 1)
    assert abs(t[0]) < 1e-15 and abs(t[-1] - 1.0) < 1e-15
    assert abs(x[0, 0]) < 1e-15
    t2, x2 = brownian_motion(1.0, 50, dim=3, x0=1.0, seed=0)
    assert x2.shape == (51, 3)
    assert np.allclose(x2[0], 1.0)
    try:
        brownian_motion(0.0, 10)
        assert False
    except ValueError:
        pass
    print("brownian self-tests passed")
