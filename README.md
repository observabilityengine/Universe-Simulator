# Universe Simulator

**Private computational research kernel**

`observabilityengine/Universe-Simulator`

A large collection of independently executable, original Python modules covering algorithms, numerical methods, evolutionary computation, physics, quantitative finance, machine learning, signal processing, data structures, control theory, cryptography (research-only), graph algorithms, number theory, statistics, and core infrastructure.

Every module is **complete**, **self-contained**, and **verified** by its own executable self-tests (`if __name__ == "__main__"` with real asserts).

---

## Project Policy — Production-Ready Only

This repository enforces a strict quality bar. Every module **must** satisfy all of the following:

- **Complete end-to-end implementation** — full, real, correct algorithm from start to finish
- **Runnable and self-testing** — working `if __name__ == "__main__"` block with real asserts (happy path + edge cases)
- **Functionally verified** — numerically checked against known references or mathematical properties where applicable
- **Original** — written from scratch for this repository; no borrowed, cloned, or proprietary code

### Explicitly forbidden

- Skeletons, scaffolding, stubs, or placeholders
- Pseudo-code
- `NotImplementedError` for the general case
- Demo-only or restricted versions that silently under-implement the algorithm
- Incomplete logic disguised as "educational" or "simplified" without clear, documented scope limits

Any genuine scope limitation (e.g. "assumes input fits in memory", "educational KDF — not for production secrets") must be stated clearly in the module docstring. Scope limits are never an excuse for incomplete code.

---

## Security Policy

**Full policy:** [SECURITY.md](SECURITY.md)

Key points:

- This is a **private research repository**. It is not a production service, network-facing application, or multi-user system.
- Cryptographic and security-related modules (`crypto/`, `security/`) are for **research and educational purposes only**. They are **not** formally audited for production use with real secrets.
- Never unpickle data from untrusted sources (`core/state.py` uses `pickle` for checkpoints).
- Report security-relevant issues **privately** to the repository owner. Do not open public issues for vulnerabilities.
- Only the `main` branch is supported.

---

## Repository Structure

| Package | Domain |
|---------|--------|
| `agi/` | Agent, planning, and memory components |
| `cache/` | Caching algorithms (ARC, LFU, …) |
| `compress/` | Compression (Huffman, LZ77/78, arithmetic coding, BWT, RLE, …) |
| `control/` | Control theory (PID, LQR, LQG, Kalman, MPC, pole placement, …) |
| `core/` | Core infrastructure (scheduler, event bus, lock-free structures, …) |
| `crypto/` | Research cryptographic primitives and hashes (not production-audited) |
| `data/` | Advanced data structures (trees, tries, skip lists, union-find, LRU, sketches, …) |
| `dist/` | Distributed systems primitives |
| `evolution/` | Evolutionary computation and swarm intelligence (DE, NSGA-II, GWO, CMA-ES, MAP-Elites, …) |
| `finance/` | Quantitative finance (Black-Scholes, binomial trees, bonds, yield curves, …) |
| `geometry/` | Computational geometry (Delaunay, …) |
| `graph/` | Graph algorithms (shortest paths, max-flow/Dinic, matching, SCC, MST/Kruskal, Louvain, betweenness, coloring, …) |
| `knowledge/` | Knowledge representation |
| `logic/` | Logic, SAT, resolution |
| `mathlib/` | Numerical linear algebra (CG, QR, Cholesky, LU, SVD, determinants, PCA, …) |
| `matrix/` | Sparse and dense matrix formats / factorizations |
| `ml/` | Machine learning (CART, random forest, gradient boosting, k-NN, naive Bayes, k-means, DBSCAN, PCA, …) |
| `net/` | Networking utilities (rate limiting, circuit breaker, …) |
| `numtheory/` | Number theory (Miller-Rabin, Pollard's Rho, sieve, extended GCD, …) |
| `observability/` | Metrics, tracing, histograms |
| `optim/` | Optimizers (Adam, L-BFGS, simulated annealing, Nelder-Mead, Powell, …) |
| `physics/` | Physics simulations (Ising, Verlet MD, heat/wave equations, pendulum, …) |
| `protocol/` | Protocol parsers |
| `quant/` | Quantitative models (Heston, Merton jump-diffusion, …) |
| `search/` | Search algorithms |
| `security/` | Password hashing, HMAC helpers (research-only) |
| `signal/` | Signal processing (FFT, wavelets, Hilbert, convolution, Savitzky-Golay, median filter, …) |
| `sort/` | Sorting algorithms |
| `stats/` | Statistics and sampling (Metropolis-Hastings, HMM, bootstrap, KDE, KS test, linear regression, …) |
| `string/` | String algorithms (KMP, Z-algorithm, suffix structures, edit distance, …) |

---

## Evolution Package

The `evolution/` package contains original implementations of evolutionary and swarm algorithms, including:

- Differential Evolution (classic, adaptive, current-to-best)
- Evolution Strategies and simplified CMA-ES
- NSGA-II and SPEA2 (multi-objective)
- Grey Wolf, Whale, Firefly, Artificial Bee Colony, Ant Colony
- Island Model GA, Memetic Algorithm, Cultural Algorithm
- Novelty Search, MAP-Elites
- Genetic Programming, Stochastic Ranking, Co-evolution

---

## How to Run

Each module is self-contained and runnable:

```bash
python -m evolution.differential_evolution
python -m evolution.nsga2
python -m evolution.grey_wolf
python -m ml.cart
python -m ml.pca
python -m graph.dinic
python -m graph.louvain
python -m optim.lbfgs
python -m optim.adam
python -m physics.ising
python -m signal.fft
python -m stats.metropolis_hastings
python -m numtheory.miller_rabin
python -m finance.black_scholes
python -m finance.binomial_option
python -m string.kmp
python -m mathlib.conjugate_gradient
```

Or run the top-level entry point (if present):

```bash
python main.py
```

Every module includes an `if __name__ == "__main__"` block that executes real assertions covering both the happy path and edge cases.

---

## Principles

1. **Accuracy over claims** — only ship code that actually runs and is correct.
2. Only modules that exist in the repository are documented.
3. Implementations are original and self-contained (standard library preferred; NumPy/SciPy only where required and declared).
4. Prefer verifiable numerical results over narrative claims.
5. Security-sensitive modules are research-only; consult [SECURITY.md](SECURITY.md) before any reuse.
6. Production-ready, start-to-finish, complete code only — no skeletons, no scaffolding, no placeholders, no stubs.

---

## License & Access

Private repository. All rights reserved by the owner. Do not redistribute modules outside the authorized context.
