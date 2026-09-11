# Universe Simulator – Module Catalog

Every Python module present in the repository is intended to be a complete, original, self-contained implementation that includes an executable self-test (`if __name__ == "__main__"`).

**Approximate module count (excluding `__init__.py`): ~450+**

---

## Package Index (top-level)

| Package | Domain summary |
|---------|----------------|
| `agi/` | Agent, planner, memory |
| `bayes/` | Conjugate priors, MH, Gibbs, HMC, NUTS, VI, Bayesian linear/logistic |
| `bio/` | Needleman–Wunsch, Smith–Waterman, UPGMA, neighbour-joining, HMM genomics, PCR |
| `cache/` | ARC, LFU |
| `compiler/` | Lexer, parser, AST, interpreter, bytecode, optimisations, REPL |
| `compress/` | Huffman, LZ, arithmetic coding, BWT, RLE |
| `consensus/` | Consensus protocol primitives |
| `control/` | PID, LQR, LQG, Kalman, MPC, pole placement |
| `core/` | Scheduler, event bus, lock-free queue, observability, state serializer |
| `cosmology/` | Friedmann, ΛCDM, CMB, cosmic web, primordial perturbations |
| `crypto/` | Research cryptographic primitives (non-production) |
| `crypto_adv/` | RSA, DH, ECC/ECDSA, ChaCha20, AES, HKDF, Poly1305, Merkle, Shamir, Schnorr |
| `dark/` | Halo finder/formation, dark energy, modified gravity |
| `data/` | Trees, tries, skip lists, union-find, sketches, entity store |
| `database/` | B+ tree, WAL, query planner, buffer pool, MVCC |
| `dist/` | Distributed systems primitives |
| `dl/` | Pure-Python autograd tensor, layers, optimizers, CNN/RNN/LSTM/GRU, attention, train loop |
| `evolution/` | DE, NSGA-II, SPEA2, CMA-ES, GWO, MAP-Elites, GP, co-evolution, mutator |
| `finance/` | Black–Scholes, binomial trees, bonds, yield curves |
| `formal/` | Formal / SAT utilities |
| `geo/` | Geohash, Haversine/Vincenty, UTM, KD/ball/quad trees |
| `geometry/` | Computational geometry |
| `graph/` | Shortest paths, max-flow, matching, SCC, MST, community detection |
| `graphics/` | Ray tracer, rasterizer, shading, mesh loaders |
| `hydro/` | SPH, EOS, cooling, star formation, stellar evolution, black hole |
| `image/` | Filtering, edges, morphology, feature detectors, stitching |
| `knowledge/` | Knowledge representation |
| `logic/` | Logic / resolution |
| `mathlib/` | Factorizations, determinants, PCA helpers |
| `matrix/` | Sparse/dense matrix formats |
| `ml/` | CART, forests, boosting, k-NN, clustering, PCA |
| `nbody/` | Symplectic integrators, Barnes–Hut, particle-mesh, adaptive, PN, geodesics |
| `net/` | Rate limiting, circuit breaker |
| `nlp/` | Tokenization, TF-IDF, embeddings, POS/NER, transformers |
| `numtheory/` | Primality, factoring, sieves, GCD |
| `observability/` | Metrics, tracing, histograms |
| `optim/` | Adam, L-BFGS, annealing, Nelder–Mead, Powell |
| `physics/` | N-body, Ising, Verlet MD, PDEs, oscillators, fractals, symbolic mechanics |
| `planetary/` | Collisions, tides, climate, atmospheric escape |
| `protocol/` | Protocol parsers |
| `quant/` | Heston, jump-diffusion |
| `quantum/` | Qubit state, gates, circuit, QFT, VQE |
| `rl/` | MDP, value/policy iteration, Q-learning, SARSA, actor-critic, DQN |
| `search/` | Search algorithms |
| `security/` | Password hashing / HMAC helpers (research-only) |
| `sigproc/` | FFT, wavelets, Hilbert, convolution (renamed from `signal/`) |
| `sort/` | Sorting algorithms |
| `stats/` | MH, HMM, bootstrap, KDE, tests, regression |
| `stringalgo/` | KMP, Z-algorithm, suffix, edit distance (renamed from `string/`) |
| `symbolic/` | Symbolic computation helpers |
| `timeseries/` | ARIMA family, smoothing, ADF, GARCH, Granger, change-point |

---

## Audit status (2026-09-11)

- Structural fix applied: `physics/__init__.py` no longer imports non-existent symbols.
- Representative self-tests executed and passed (friedmann, lockfree_queue, needleman_wunsch, plus inspection of nbody, dl/tensor, quantum/qubit, crypto_adv/rsa, evolution/mutator).
- No `NotImplementedError` / placeholder stubs located in searchable surface.
- Documentation (PHYSICS_MODULES.md, DUE_DILIGENCE.md) updated to match current code.

For the authoritative live listing of every file, use the repository tree or `git ls-files '*.py'`.
