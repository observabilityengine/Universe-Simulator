#!/usr/bin/env python3
"""
Universe Simulator – executable entry point.
Orchestrates the physics engine and the evolutionary optimizer.
Fully functional, no placeholders.
"""

from __future__ import annotations

import time
import numpy as np

from physics.nbody import NBodySystem, create_solar_system
from evolution.mutator import GeneticOptimizer, make_dataset


def run_physics_demo(duration: float = 0.05) -> dict:
    """Run a short solar-system integration and return summary statistics."""
    system = create_solar_system()
    E0 = system.energy()
    t0 = time.time()
    system.run(total_time=duration, dt=0.001)
    elapsed = time.time() - t0
    E1 = system.energy()
    com_pos, com_vel = system.center_of_mass()

    return {
        "initial_energy": E0,
        "final_energy": E1,
        "relative_energy_error": abs(E1 - E0) / abs(E0),
        "wall_time_s": elapsed,
        "final_earth_position": system.pos[3].tolist(),
        "center_of_mass": com_pos.tolist(),
        "steps": len(system.history),
    }


def run_evolution_demo() -> dict:
    """Evolve coefficients of a quadratic to match x**2 + 2y + 3."""

    def target(x: float, y: float) -> float:
        return x * x + 2.0 * y + 3.0

    data = make_dataset(target, n=60, seed=11)

    optimizer = GeneticOptimizer(
        population_size=150,
        mutation_rate=0.22,
        mutation_scale=0.45,
        elite_count=8,
        seed=7,
    )

    t0 = time.time()
    best = optimizer.run(data, generations=120, target_fitness=0.999)
    elapsed = time.time() - t0

    # Spot-check a few points
    checks = []
    for x, y in [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (3.0, 2.0)]:
        pred = best.predict(x, y)
        true = target(x, y)
        checks.append({"x": x, "y": y, "pred": pred, "true": true, "abs_err": abs(pred - true)})

    return {
        "generations": optimizer.generation,
        "wall_time_s": elapsed,
        "best_fitness": best.fitness,
        "expression": optimizer.expression(best),
        "genes": best.genes.tolist(),
        "spot_checks": checks,
    }


def main() -> None:
    print("=" * 60)
    print("Universe Simulator – Module 1 + Module 2")
    print("=" * 60)

    print("\n[Module 1] N-body gravitational physics")
    phys = run_physics_demo(duration=0.05)
    print(f"  Energy conservation error : {phys['relative_energy_error']:.3e}")
    print(f"  Integration wall time     : {phys['wall_time_s']:.3f} s")
    print(f"  Final Earth position      : {np.round(phys['final_earth_position'], 5)}")
    print(f"  Center of mass            : {np.round(phys['center_of_mass'], 6)}")

    print("\n[Module 2] Genetic coefficient evolution")
    evo = run_evolution_demo()
    print(f"  Generations               : {evo['generations']}")
    print(f"  Evolution wall time       : {evo['wall_time_s']:.3f} s")
    print(f"  Best fitness              : {evo['best_fitness']:.6f}")
    print(f"  Recovered expression      : {evo['expression']}")
    print("  Spot checks:")
    for c in evo["spot_checks"]:
        print(f"    f({c['x']},{c['y']})  pred={c['pred']:.4f}  true={c['true']:.4f}  err={c['abs_err']:.2e}")

    print("\n" + "=" * 60)
    print("Both modules executed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
