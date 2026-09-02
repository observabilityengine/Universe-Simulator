# Universe Simulator

Private computational research kernel.

A collection of independently executable, original Python modules spanning physics, quantitative finance, algorithms, machine learning, signal processing, networking, security, geometry, and core infrastructure.

**Repository:** `observabilityengine/Universe-Simulator` (private)

---

## Project Policy

- **Original code only** — every module was written from scratch for this repository.
- **No stubs, no skeletons, no placeholders, no pseudo-code.**
- **Every module is runnable** — each file has a working `if __name__ == "__main__"` self-test.
- **Numerically verified** where applicable (energy conservation, put-call parity, residual norms, etc.).
- **No external proprietary code** was copied or borrowed.

See also: [SECURITY.md](SECURITY.md)

---

## Package Inventory (accurate as of latest push)

| Package | Modules present |
|---------|-----------------|
| **agi/** | `agent.py`, `memory.py` |
| **cache/** | `lfu.py` |
| **compress/** | `huffman.py` |
| **control/** | `pid.py`, `kalman.py`, `fsm.py`, `lqr.py` |
| **core/** | `scheduler.py`, `observability.py`, `event_log.py`, `state.py`, `clock.py`, `priority_queue.py` |
| **crypto/** | `merkle.py`, `hashchain.py`, `pure_sha256.py` |
| **data/** | `bitarray.py`, `bloom.py`, `interval_tree.py`, `lru.py`, `unionfind.py`, `skiplist.py`, `spatial_hash.py`, `entity_store.py`, `octree.py`, `kd_tree.py`, `btree.py`, `segment_tree.py`, `trie.py` |
| **evolution/** | `mutator.py`, `genetic.py` |
| **finance/** | `irr.py`, `bond.py`, `black76.py`, `duration.py` |
| **geometry/** | `convex_hull.py`, `aabb.py`, `raycast.py` |
| **graph/** | `dijkstra.py`, `bellman_ford.py`, `toposort.py`, `floyd_warshall.py`, `kruskal.py`, `prim.py` |
| **knowledge/** | `graph.py` |
| **logic/** | `sat_solver.py` |
| **matrix/** | `lu.py`, `qr.py`, `eigen.py` |
| **ml/** | `numpy_net.py`, `bayes.py`, `kmeans.py`, `perceptron.py` |
| **net/** | `rate_limiter.py`, `circuit_breaker.py`, `retry.py`, `token_bucket.py` |
| **observability/** | `metrics.py`, `tracer.py` |
| **optim/** | `gradient.py`, `adam.py`, `sgd.py`, `rmsprop.py` |
| **physics/** | `nbody.py`, `fractal.py`, `symbolic.py`, `integrator.py`, `collision.py`, `softbody.py`, `sph.py`, `gravity.py`, `barnes_hut.py` |
| **protocol/** | `http_parser.py` |
| **quant/** | `black_scholes.py`, `monte_carlo.py`, `binomial_tree.py`, `portfolio.py`, `heston.py`, `vasicek.py`, `cir.py` |
| **search/** | `astar.py`, `rrt.py`, `beam_search.py` |
| **security/** | `password.py`, `hmac_auth.py` |
| **signal/** | `fft_filter.py`, `wavelet.py`, `convolution.py` |
| **stats/** | `regression.py`, `bootstrap.py`, `distribution.py`, `hypothesis.py`, `kernel_density.py`, `pca.py` |
| **string/** | `kmp.py`, `edit_distance.py`, `rabin_karp.py`, `suffix_array.py`, `aho_corasick.py` |

Root: `main.py`, `README.md`, `SECURITY.md`, `.gitignore`

---

## Run

Every module is independently executable:

```bash
python -m physics.nbody
python -m quant.black_scholes
python -m data.spatial_hash
python -m physics.barnes_hut
python -m crypto.pure_sha256
# etc.
```

Full system demonstration (when fully wired):

```bash
python main.py
```

---

## Principles

1. Accuracy over completeness claims.
2. Only modules that exist in this repository are listed above.
3. All implementations are original and self-contained.
4. Prefer verifiable numerical results over narrative claims.
5. Security-sensitive modules are for research; see SECURITY.md before reuse.
