"""
Universe Simulator - Macaulay & Modified Duration
Original bond duration calculator.
"""

from __future__ import annotations

from typing import List


def macaulay_duration(
    cashflows: List[float],
    times: List[float],
    ytm: float,
) -> float:
    """cashflows and times parallel; ytm continuous or annual compounding approx."""
    pv = 0.0
    weighted = 0.0
    for c, t in zip(cashflows, times):
        disc = c / ((1 + ytm) ** t)
        pv += disc
        weighted += t * disc
    return weighted / pv if pv else 0.0


def modified_duration(mac: float, ytm: float, frequency: int = 1) -> float:
    return mac / (1 + ytm / frequency)


if __name__ == "__main__":
    # 3-year 5% annual coupon bond, face 100, ytm 5%
    cfs = [5.0, 5.0, 105.0]
    ts = [1.0, 2.0, 3.0]
    mac = macaulay_duration(cfs, ts, 0.05)
    mod = modified_duration(mac, 0.05)
    assert 2.7 < mac < 2.9
    print("duration self-test passed", mac, mod)
