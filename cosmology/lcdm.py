"""LCDM parameter engine – derived quantities from cosmological parameters."""
from __future__ import annotations
import math
from dataclasses import dataclass
from .friedmann import hubble, cosmic_age, comoving_distance


@dataclass
class LCDMParams:
    H0: float = 67.4
    Om: float = 0.315
    Ol: float = 0.685
    Ob: float = 0.049
    Or: float = 9.0e-5
    ns: float = 0.965
    sigma8: float = 0.811

    @property
    def Ok(self) -> float:
        return 1.0 - self.Om - self.Ol - self.Or

    @property
    def h(self) -> float:
        return self.H0 / 100.0

    @property
    def age_Gyr(self) -> float:
        return cosmic_age(self.Om, self.Ol, self.H0, self.Or)

    def H(self, z: float) -> float:
        a = 1.0 / (1 + z)
        return hubble(a, self.Om, self.Or, self.Ol, self.H0)

    def critical_density(self, z: float = 0.0) -> float:
        H = self.H(z)
        h_z = H / 100.0
        return 2.775e11 * h_z * h_z

    def angular_diameter_distance(self, z: float) -> float:
        return comoving_distance(z, self.Om, self.Ol, self.H0) / (1 + z)

    def luminosity_distance(self, z: float) -> float:
        return comoving_distance(z, self.Om, self.Ol, self.H0) * (1 + z)


if __name__ == "__main__":
    p = LCDMParams()
    assert abs(p.Ok) < 0.01
    assert 12 < p.age_Gyr < 15
    assert p.H(0) == p.H0
    print(f"lcdm age={p.age_Gyr:.2f} Om={p.Om} D_A(1)={p.angular_diameter_distance(1):.0f}")
    print("lcdm self-tests passed")
