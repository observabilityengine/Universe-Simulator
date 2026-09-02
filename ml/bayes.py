"""
Module 22 – Bayesian Updater
Exact Bayesian inference for discrete and Beta-Bernoulli models.
Original, executable implementation.
"""

from __future__ import annotations
import math
from typing import Dict, List, Hashable, Optional


class DiscreteBayes:
    def __init__(self, hypotheses: List[Hashable], priors: Optional[Dict[Hashable, float]] = None):
        self.hypotheses = list(hypotheses)
        if priors:
            total = sum(priors.values())
            self.posterior = {h: priors.get(h, 0.0) / total for h in self.hypotheses}
        else:
            n = len(self.hypotheses)
            self.posterior = {h: 1.0 / n for h in self.hypotheses}

    def update(self, likelihoods: Dict[Hashable, float]) -> Dict[Hashable, float]:
        unnorm = {}
        for h in self.hypotheses:
            unnorm[h] = self.posterior[h] * likelihoods.get(h, 0.0)
        total = sum(unnorm.values())
        if total == 0:
            return self.posterior
        self.posterior = {h: v / total for h, v in unnorm.items()}
        return dict(self.posterior)

    def map(self) -> Hashable:
        return max(self.posterior, key=self.posterior.get)

    def entropy(self) -> float:
        e = 0.0
        for p in self.posterior.values():
            if p > 0:
                e -= p * math.log2(p)
        return e


class BetaBernoulli:
    def __init__(self, alpha: float = 1.0, beta: float = 1.0):
        self.alpha = alpha
        self.beta = beta

    def update(self, successes: int, trials: int) -> None:
        failures = trials - successes
        self.alpha += successes
        self.beta += failures

    def mean(self) -> float:
        return self.alpha / (self.alpha + self.beta)

    def variance(self) -> float:
        a, b = self.alpha, self.beta
        return (a * b) / ((a + b) ** 2 * (a + b + 1))


if __name__ == "__main__":
    print("Testing Bayesian Updater...")
    bayes = DiscreteBayes(["healthy", "disease"], {"healthy": 0.99, "disease": 0.01})
    bayes.update({"healthy": 0.05, "disease": 0.9})
    print(f"  After positive test: {bayes.posterior}")
    print(f"  MAP: {bayes.map()}  entropy: {bayes.entropy():.3f}")
    bb = BetaBernoulli(1, 1)
    bb.update(successes=7, trials=10)
    print(f"  BetaBernoulli mean: {bb.mean():.3f}  var: {bb.variance():.4f}")
    print("Bayesian Updater module OK.")
