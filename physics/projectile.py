"""Projectile motion under constant gravity (no drag).

Complexity: O(1) analytic; O(steps) trajectory sample.
Original implementation.
"""
from __future__ import annotations

import math
from typing import List, Tuple


def range_distance(v0: float, angle_deg: float, g: float = 9.81) -> float:
    """Horizontal range on flat ground."""
    theta = math.radians(angle_deg)
    return (v0 * v0 * math.sin(2 * theta)) / g


def time_of_flight(v0: float, angle_deg: float, g: float = 9.81) -> float:
    theta = math.radians(angle_deg)
    return 2 * v0 * math.sin(theta) / g


def max_height(v0: float, angle_deg: float, g: float = 9.81) -> float:
    theta = math.radians(angle_deg)
    return (v0 * math.sin(theta)) ** 2 / (2 * g)


def trajectory(
    v0: float,
    angle_deg: float,
    steps: int = 50,
    g: float = 9.81,
) -> List[Tuple[float, float]]:
    """Sample (x, y) points from launch to landing."""
    T = time_of_flight(v0, angle_deg, g)
    theta = math.radians(angle_deg)
    pts: List[Tuple[float, float]] = []
    for i in range(steps + 1):
        t = T * i / steps
        x = v0 * math.cos(theta) * t
        y = v0 * math.sin(theta) * t - 0.5 * g * t * t
        pts.append((x, max(0.0, y)))
    return pts


if __name__ == "__main__":
    R = range_distance(10.0, 45.0)
    assert abs(R - 10.0 ** 2 / 9.81) < 1e-9
    assert abs(time_of_flight(10.0, 90.0) - 20.0 / 9.81) < 1e-9
    assert max_height(10.0, 90.0) > max_height(10.0, 45.0)
    traj = trajectory(10.0, 45.0, 20)
    assert traj[0] == (0.0, 0.0)
    assert abs(traj[-1][1]) < 1e-9
    print("projectile self-tests passed")
