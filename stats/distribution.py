"""
Module 56 – Statistical Distributions
Normal, Exponential, Poisson sampling + PDF/CDF.
Complete implementation without scipy.stats.
"""

from __future__ import annotations
import math
import random


def normal_pdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    return math.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * math.sqrt(2 * math.pi))


def normal_cdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    z = (x - mu) / sigma
    t = 1.0 / (1.0 + 0.2316419 * abs(z))
    d = 0.3989423 * math.exp(-z * z / 2.0)
    p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))))
    return 1.0 - p if z > 0 else p


def normal_sample(mu: float = 0.0, sigma: float = 1.0) -> float:
    u1 = random.random()
    u2 = random.random()
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return mu + sigma * z


def exponential_sample(lambd: float = 1.0) -> float:
    return -math.log(1.0 - random.random()) / lambd


def poisson_sample(lam: float) -> int:
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1


def poisson_pmf(k: int, lam: float) -> float:
    if k < 0:
        return 0.0
    return math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1))


if __name__ == "__main__":
    print("Testing Statistical Distributions...")
    random.seed(42)
    samples = [normal_sample(5, 2) for _ in range(10000)]
    mean = sum(samples) / len(samples)
    var = sum((x - mean) ** 2 for x in samples) / len(samples)
    print(f"  Normal(5,2) sample mean={mean:.3f} std={math.sqrt(var):.3f}")
    print(f"  N(0,1) PDF(0)={normal_pdf(0):.6f}")
    print(f"  N(0,1) CDF(1.96)={normal_cdf(1.96):.4f}")
    exp_s = [exponential_sample(2.0) for _ in range(5000)]
    print(f"  Exp(2) mean={sum(exp_s)/len(exp_s):.3f} (true 0.5)")
    pois = [poisson_sample(4.0) for _ in range(5000)]
    print(f"  Poisson(4) mean={sum(pois)/len(pois):.3f}")
    print(f"  Poisson(4) P(3)={poisson_pmf(3, 4):.4f}")
    print("Statistical Distributions module OK.")
