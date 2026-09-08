# Test Suites

**Universe Simulator**

Every module ships with its own executable self-test. There is no external test-framework dependency; tests are ordinary Python assertions executed when the module is run as `__main__`.

---

## 1. Philosophy

- **Self-contained** – each module verifies itself.
- **Real asserts** – numerical results, edge cases, invariants, and known reference values.
- **No mocks for core logic** – the algorithm under test is the real implementation.
- **Fast** – majority of self-tests finish in < 1 s; Monte-Carlo and evolutionary tests are capped at a few seconds.
- **Deterministic where possible** – fixed seeds for RNG-driven algorithms.

---

## 2. How a Self-Test Looks

```python
if __name__ == "__main__":
    result = some_function(known_input)
    assert abs(result - expected) < 1e-6, result
    assert invariant_holds(result)
    print("module_name self-tests passed")
```

---

## 3. Running the Suites

### Single module
```bash
python -m package.module
```

### Whole package (example)
```bash
for m in control/*.py; do
  [[ $m == *__init__* ]] && continue
  python -m control.$(basename ${m%.py}) || echo FAIL $m
done
```

### Top-level smoke test
```bash
python main.py
```

### Recommended minimal CI set
```bash
python main.py
python -m control.pid
python -m control.pole_placement
python -m optim.cmaes
python -m optim.adam
python -m stats.metropolis_hastings
python -m quant.black_scholes
python -m physics.ising
python -m data.skip_list
python -m graph.push_relabel
python -m mathlib.qr_householder
```

---

## 4. Coverage by Domain

| Package   | Typical assertions                                           |
|-----------|--------------------------------------------------------------|
| control   | closed-loop error → 0, pole locations, energy bounds         |
| optim     | reaches known minimum of sphere / Rosenbrock                 |
| stats     | sample mean / variance within statistical tolerance          |
| quant     | option price brackets Black-Scholes / known references       |
| physics   | energy conservation, magnetization, bound orbits             |
| data      | insert/search/delete correctness, order statistics           |
| graph     | max-flow value, shortest-path distances, connectivity        |
| mathlib   | reconstruction error, orthogonality, singular values         |
| signal    | perfect reconstruction (wavelets), energy preservation       |
| evolution | fitness improvement, convergence on test functions           |
| compress  | lossless round-trip                                          |
| crypto*   | known test vectors (educational only)                        |

\* crypto and security modules are research-only; see SECURITY.md.

---

## 5. Adding a New Module – Test Requirements

A new module is not complete until:

1. It contains a non-trivial `if __name__ == "__main__"` block.
2. The block exercises both the happy path and at least one edge case.
3. Assertions are quantitative rather than mere “no exception”.
4. The test terminates with a clear success message.
5. Running the module from the repository root succeeds with exit code 0.

---

## 6. Interpreting Failures

- `AssertionError` with a printed value → examine the numeric discrepancy.
- Timeout / hang → reduce iteration counts in the `__main__` block.
- Import errors → confirm working directory is the repository root.

See TROUBLESHOOTING.md for detailed recovery steps.

---

## 7. Determinism

Modules that use randomness accept an explicit `seed` argument. Self-tests always pass a fixed seed so that results are reproducible.

---

*This document is the authoritative description of how correctness is verified inside the Universe Simulator repository.*
