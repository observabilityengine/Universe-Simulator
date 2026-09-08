# Operations Guide

**Universe Simulator – Private Computational Research Kernel**

This document describes how to run, monitor, and maintain the repository in day-to-day use.

---

## 1. Environment Requirements

- Python 3.10 or newer (CPython recommended)
- Standard library only for the majority of modules
- Optional: NumPy for a small number of numerical modules that declare it
- No external services, databases, or network endpoints are required for core execution

```bash
python --version   # must be >= 3.10
```

---

## 2. Running Individual Modules

Every module is self-contained and executable:

```bash
python -m package.module_name
# examples
python -m control.pid
python -m evolution.differential_evolution
python -m quant.black_scholes
python -m physics.ising
python -m stats.metropolis_hastings
python -m optim.cmaes
python -m data.skip_list
```

Each run executes the module’s `if __name__ == "__main__"` block, which contains real assertions covering happy-path and edge cases. A successful run ends with a confirmation message such as `... self-tests passed`.

---

## 3. Top-Level Entry Point

```bash
python main.py
```

Runs a short N-body gravitational integration followed by a genetic-coefficient evolution demonstration and prints energy-conservation and fitness metrics.

---

## 4. Batch Verification

To exercise a whole package:

```bash
# example – control package
for f in control/*.py; do
  [ "$(basename $f)" = "__init__.py" ] && continue
  python -m control.$(basename $f .py) || echo "FAIL $f"
done
```

---

## 5. Performance Expectations

- Most modules finish self-tests in well under one second on a modern CPU.
- Monte-Carlo and evolutionary modules may take a few seconds depending on path/generation count.
- Memory footprint is modest.

---

## 6. Logging & Observability

The `core.observability` and `core.event_log` modules provide structured logging and metrics collection when integrated. For ordinary self-tests, stdout is sufficient.

---

## 7. Checkpointing

`core.state` supports pickle-based checkpoints. Never unpickle data from untrusted sources (see SECURITY.md).

---

## 8. Continuous Integration (Recommended)

A minimal smoke-test set:

```bash
python main.py
python -m control.pid
python -m optim.cmaes
python -m stats.metropolis_hastings
python -m quant.black_scholes
python -m physics.ising
```

---

## 9. Operational Hygiene

- Keep the `main` branch clean; only complete, self-testing modules are merged.
- Do not commit secrets or large binary data.
- Prefer pure-Python implementations; declare any NumPy dependency explicitly.
- After adding a new module, always run its self-test before pushing.

---

*Last updated to match repository policy of production-ready, original, self-testing code only.*
