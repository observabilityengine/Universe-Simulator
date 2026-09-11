# Universe Simulator

**Open-source computational research kernel**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`observabilityengine/Universe-Simulator`

A large collection of independently executable, original Python modules covering numerical physics, cosmology, deep learning, time series, NLP, Bayesian statistics, computational biology, cryptography (research-only), graphics, compilers, geospatial algorithms, reinforcement learning, database internals, and core scientific infrastructure.

Every module is **complete**, **self-contained**, and **verified** by its own executable self-tests (`if __name__ == "__main__"` with real asserts).

---

## Project Policy — Complete & Runnable Only

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

- This is a research kernel, not a production service, network-facing application, or multi-user system.
- Cryptographic and security-related modules (`crypto/`, `crypto_adv/`, `security/`) are for **research and educational purposes only**. They are **not** formally audited for production use with real secrets.
- Never unpickle data from untrusted sources (`core/state.py` uses `pickle` for checkpoints).
- Report security-relevant issues via a [GitHub Security Advisory](https://github.com/observabilityengine/Universe-Simulator/security/advisories/new) when possible, or contact maintainers privately.
- Only the `main` branch is supported.

---

## Naming note (stdlib collisions)

Top-level package names **must not** collide with the Python standard library. Former packages `string/` and `signal/` were renamed:

| Old (removed) | New |
|---------------|-----|
| `string/` | `stringalgo/` |
| `signal/` | `sigproc/` |

Import as `from stringalgo.kmp import kmp_search` and `from sigproc.fft import fft`.

---

## Repository Structure

### Numerical Physics & Cosmology

| Package | Domain |
|---------|--------|
| `nbody/` | N-body gravitational integrators, symplectic schemes, Barnes–Hut, particle-mesh |
| `cosmology/` | Friedmann equations, ΛCDM scale-factor evolution, cosmic distances |
| `hydro/` | SPH hydrodynamics, equation of state, cooling/heating |
| `planetary/` | Collision solvers, tidal heating, climate/energy-balance models |
| `dark/` | Dark-matter particle engines, halo formation, subhalo detection |
| `physics/` | Ising model, Verlet MD, heat/wave equations, pendulum |
| `quantum/` | Quantum simulation primitives |

### Machine Learning & Statistics

| Package | Domain |
|---------|--------|
| `dl/` | Pure-Python autograd tensor engine, layers, optimizers, CNN/RNN/LSTM/GRU, attention, transformer blocks, training loop |
| `ml/` | CART, random forest, gradient boosting, k-NN, naive Bayes, k-means, DBSCAN, PCA |
| `bayes/` | Conjugate priors, Metropolis–Hastings, Gibbs, HMC, NUTS, variational inference, Bayesian linear/logistic, LOO-CV |
| `timeseries/` | AR/MA/ARMA/ARIMA/SARIMA, exponential smoothing, Holt–Winters, ADF, ACF/PACF, GARCH, Granger causality, change-point, anomaly detection |
| `rl/` | MDP, value/policy iteration, Q-learning, SARSA, actor-critic, DQN |
| `stats/` | Metropolis–Hastings, HMM, bootstrap, KDE, KS test, linear regression |
| `optim/` | Adam, L-BFGS, simulated annealing, Nelder–Mead, Powell |

### Language, Vision & Graphics

| Package | Domain |
|---------|--------|
| `nlp/` | Tokenization, stemming, lemmatization, TF-IDF, word2vec, GloVe, POS/NER, sentiment, topic modeling, BPE, transformer LM |
| `image/` | Grayscale, histogram equalization, Gaussian blur, Sobel/Canny, morphology, Hough, SIFT/SURF/ORB, homography, stitching |
| `graphics/` | Ray tracer, rasterizer, z-buffer, Blinn–Phong/Phong, texture/UV mapping, mesh/OBJ/STL loaders, SSAO, depth-of-field, antialiasing |

### Systems, Compilers & Data

| Package | Domain |
|---------|--------|
| `compiler/` | Lexer, recursive-descent parser, AST, interpreter, bytecode, constant folding, DCE, type checker, REPL, JIT |
| `database/` | B+ tree, WAL, query planner, SQL parser, buffer pool, MVCC, row/column stores |
| `data/` | Trees, tries, skip lists, union-find, LRU, sketches |
| `core/` | Scheduler, event bus, lock-free structures |
| `dist/` | Distributed systems primitives |
| `consensus/` | Consensus protocols |
| `cache/` | ARC, LFU, and related caches |
| `net/` | Rate limiting, circuit breaker |

### Scientific Domains

| Package | Domain |
|---------|--------|
| `bio/` | Needleman–Wunsch, Smith–Waterman, UPGMA, neighbor-joining, HMM genomics, ORF prediction, restriction enzymes, PCR simulation |
| `geo/` | Geohash, H3-style index, Haversine/Vincenty, UTM, WGS84/ECEF, KD-tree, ball tree, quadtree, spatial join |
| `crypto_adv/` | RSA, Diffie–Hellman, ECC/ECDSA, ChaCha20, AES, HKDF, PBKDF2, Poly1305, Merkle trees, Shamir secret sharing, Schnorr ZKP |
| `crypto/` | Research cryptographic primitives and hashes (not production-audited) |
| `security/` | Password hashing, HMAC helpers (research-only) |
| `formal/` | Formal methods / SAT-related utilities |
| `symbolic/` | Symbolic computation helpers |
| `mathlib/` | CG, QR, Cholesky, LU, SVD, determinants, PCA |
| `matrix/` | Sparse and dense matrix formats / factorizations |
| `numtheory/` | Miller–Rabin, Pollard's Rho, sieve, extended GCD |
| `sigproc/` | FFT, wavelets, Hilbert, convolution, Savitzky–Golay (renamed from `signal/` to avoid stdlib collision) |
| `stringalgo/` | KMP, Z-algorithm, suffix structures, edit distance (renamed from `string/` to avoid stdlib collision) |
| `geometry/` | Computational geometry (Delaunay, …) |
| `graph/` | Shortest paths, max-flow/Dinic, matching, SCC, MST, Louvain, betweenness, coloring |
| `sort/` | Sorting algorithms |
| `search/` | Search algorithms |
| `control/` | PID, LQR, LQG, Kalman, MPC, pole placement |
| `evolution/` | DE, NSGA-II, GWO, CMA-ES, MAP-Elites, GP, co-evolution |
| `finance/` | Black–Scholes, binomial trees, bonds, yield curves |
| `quant/` | Heston, Merton jump-diffusion |
| `compress/` | Huffman, LZ77/78, arithmetic coding, BWT, RLE |
| `logic/` | Logic, SAT, resolution |
| `knowledge/` | Knowledge representation |
| `protocol/` | Protocol parsers |
| `observability/` | Metrics, tracing, histograms |
| `agi/` | Agent, planning, and memory components |

---

## Documentation

| Document | Purpose |
|----------|---------|
| [MODULE_CATALOG.md](MODULE_CATALOG.md) | Catalog of modules with package summaries |
| [PHYSICS_MODULES.md](PHYSICS_MODULES.md) | Numerical physics module reference |
| [RARE_MODULES.md](RARE_MODULES.md) | Rare / high-complexity module notes |
| [OPERATIONS.md](OPERATIONS.md) | Operational guidance |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and fixes |
| [TEST_SUITES.md](TEST_SUITES.md) | How self-tests are structured and run |
| [FAQ.md](FAQ.md) | Frequently asked questions |
| [DUE_DILIGENCE.md](DUE_DILIGENCE.md) | Diligence notes for reviewers |
| [SECURITY.md](SECURITY.md) | Security policy |
| [LICENSE](LICENSE) | MIT License |

---

## How to Run

```bash
git clone https://github.com/observabilityengine/Universe-Simulator.git
cd Universe-Simulator
```

Each module is self-contained and runnable:

```bash
# Deep learning
python -m dl.tensor
python -m dl.train_loop
python -m dl.mlp

# Time series
python -m timeseries.arima
python -m timeseries.garch
python -m timeseries.adfuller

# NLP
python -m nlp.tfidf
python -m nlp.word2vec
python -m nlp.transformer_lm

# Physics
python -m nbody.nbody_integrator
python -m cosmology.friedmann
python -m hydro.sph

# Bayesian
python -m bayes.metropolis_hastings
python -m bayes.hamiltonian_mcmc

# Biology / geospatial / crypto (research)
python -m bio.needleman_wunsch
python -m geo.geohash
python -m crypto_adv.rsa

# Compiler / graphics / image
python -m compiler.interpreter
python -m graphics.raytracer
python -m image.canny

# String algorithms / signal processing (renamed packages)
python -m stringalgo.kmp
python -m sigproc.fft

# Classic packages
python -m evolution.differential_evolution
python -m ml.cart
python -m graph.dinic
python -m optim.lbfgs
python -m finance.black_scholes
```

Or run the top-level entry point:

```bash
python main.py
```

Every module includes an `if __name__ == "__main__"` block that executes real assertions covering both the happy path and edge cases.

---

## Deep Learning (`dl/`)

Pure-Python reverse-mode autograd engine and neural network components:

- **Core:** `tensor.py`, `autograd.py`, `init_weights.py`
- **Layers:** `linear_layer.py`, `conv2d.py`, `pooling.py`, `batch_norm.py`, `dropout.py`
- **Activations / losses:** `relu.py`, `sigmoid.py`, `softmax.py`, `mse_loss.py`, `cross_entropy_loss.py`
- **Optimizers:** `sgd_optimizer.py`, `adam_optimizer.py`
- **Models:** `sequential.py`, `mlp.py`, `cnn.py`, `rnn.py`, `lstm.py`, `gru.py`
- **Attention / residual:** `attention.py`, `transformer_block.py`, `resnet_block.py`
- **Training:** `train_loop.py`

---

## Time Series (`timeseries/`)

- Classical: AR, MA, ARMA, ARIMA, SARIMA
- Smoothing: exponential smoothing, Holt–Winters
- Diagnostics: ADF, ACF/PACF, stationarity, Granger causality
- Decomposition, change-point, anomaly detection, cross-correlation
- GARCH, VAR, Fourier features, Prophet-style model, time-series CV

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

## Principles

1. **Accuracy over claims** — only ship code that actually runs and is correct.
2. Only modules that exist in the repository are documented.
3. Implementations are original and self-contained (standard library preferred; NumPy/SciPy only where required and declared).
4. Prefer verifiable numerical results over narrative claims.
5. Security-sensitive modules are research-only; consult [SECURITY.md](SECURITY.md) before any reuse.
6. Complete, start-to-finish code only — no skeletons, no scaffolding, no placeholders, no stubs.

---

## Contributing

Issues and pull requests are welcome. Please keep new modules complete, original, and self-testing. See [TEST_SUITES.md](TEST_SUITES.md) for the expected self-test style.

---

## License

Released under the [MIT License](LICENSE).

Copyright (c) 2024–2026 observabilityengine.

Cryptographic modules remain research/educational only — see the additional notice in the LICENSE file and [SECURITY.md](SECURITY.md).
