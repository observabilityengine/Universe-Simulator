# Troubleshooting Guide

**Universe Simulator**

---

## 1. Module fails with `AssertionError` in self-test

**Cause**  
Numerical tolerance too tight for the platform, floating-point differences, or a genuine regression.

**Actions**
1. Re-run the module; transient RNG seeds can produce borderline values.
2. Check the assertion message – it usually prints the actual numeric value.
3. If systematic, examine the tolerance and widen only after confirming correctness against a known reference.
4. Ensure you are on the latest `main` commit.

---

## 2. `ModuleNotFoundError` / `ImportError`

**Cause**  
Wrong working directory or missing package `__init__.py`.

**Actions**
```bash
cd /path/to/Universe-Simulator
python -m package.module
```
Confirm every package directory contains an `__init__.py`.

---

## 3. Self-test hangs or runs extremely long

**Cause**  
High Monte-Carlo path count, evolutionary generation count, or N-body step count.

**Actions**  
Temporarily reduce `n_paths`, `n_samples`, `max_gen`, or `steps` inside the module’s `__main__` block.

---

## 4. Numerical instability / NaNs

**Cause**  
Division by zero, log of non-positive, or ill-conditioned matrices.

**Actions**  
Check input ranges. Many modules already clamp or add a small epsilon.

---

## 5. `pickle` / checkpoint errors (`core.state`)

**Cause**  
Untrusted or corrupted source, or Python version mismatch.

**Actions**  
Never unpickle untrusted data. Regenerate checkpoints with the same Python version.

---

## 6. Performance regression

**Cause**  
Accidental pure-Python loops where better complexity was expected.

**Actions**  
Profile with `python -m cProfile` and compare against the previous green commit.

---

## 7. Cryptographic modules behave unexpectedly

**Cause**  
These modules are research/educational only and are not audited for production secrets.

**Actions**  
Consult SECURITY.md. Do not use them to protect real secrets.

---

## 8. Platform-specific floating-point differences

**Cause**  
Different CPU architectures or Python builds.

**Actions**  
Assertions already use tolerances. Record the observed value and adjust only after independent verification.

---

## 9. “It worked yesterday” checklist

1. `git status` – uncommitted changes?
2. `git log -1` – expected commit?
3. Identical Python version?
4. Working directory is the repository root?
5. Re-run the exact previous command.

---

*If unresolved, capture full traceback, command line, Python version and `git rev-parse HEAD`, then raise privately with the repository owner.*
