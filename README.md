# Universe Simulator

Private research repository for a self-contained computational universe kernel.

## Modules

### 1. Physics (`physics/nbody.py`)
Real Newtonian N-body integrator.
- Adaptive ODE solver (scipy)
- Energy conservation to ~1e-15
- Includes a simplified Solar System initial condition
- Fully executable: `python -m physics.nbody`

### 2. Evolution (`evolution/mutator.py`)
Real genetic algorithm that evolves polynomial coefficients.
- Population-based search with elitism, tournament selection, crossover, mutation
- Recovers target functions from data only
- Fully executable: `python -m evolution.mutator`

## Run everything

```bash
python main.py
```

Both modules execute end-to-end with real numerical work. No placeholders, no mocks, no pseudo-code.
