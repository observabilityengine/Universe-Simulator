# Universe Simulator

Private computational research kernel.

A collection of independently executable, original Python modules spanning physics, quantitative finance, algorithms, machine learning, signal processing, networking, security, geometry, and core infrastructure.

**Repository:** `observabilityengine/Universe-Simulator` (private)

---

## Project Policy

- **Original code only** — every module was written from scratch for this repository.
- **No stubs, no skeletons, no placeholders, no pseudo-code.**
- **Every module is runnable** — each file has a working `if __name__ == "__main__"` self-test.
- **Numerically verified** where applicable.
- **No external proprietary code** was copied or borrowed.

See also: [SECURITY.md](SECURITY.md)

---

## Package Inventory (accurate as of latest push)

| Package | Modules present |
|---------|-----------------|
| **agi/** | `agent.py`, `memory.py`, `planner.py` |
| **cache/** | `lfu.py`, `arc.py` |
| **compress/** | `huffman.py`, `rle.py`, `lz77.py` |
| **control/** | `pid.py`, `kalman.py`, `fsm.py`, `lqr.py`, `bang_bang.py` |
| **core/** | `scheduler.py`, `observability.py`, `event_log.py`, `state.py`, `clock.py`, `priority_queue.py`, `ring_buffer.py`, `event_bus.py` |
| **crypto/** | `merkle.py`, `hashchain.py`, `pure_sha256.py`, `pure_md5.py` |
| **data/** | `bitarray.py`, `bloom.py`, `interval_tree.py`, `lru.py`, `unionfind.py`, `skiplist.py`, `spatial_hash.py`, `entity_store.py`, `octree.py`, `kd_tree.py`, `btree.py`, `segment_tree.py`, `trie.py`, `fenwick.py`, `sparse_table.py`, `cartesian_tree.py`, `splay.py`, `counting_bloom.py` |
| **evolution/** | `mutator.py`, `genetic.py`, `pso.py` |
| **finance/** | `irr.py`, `bond.py`, `black76.py`, `duration.py`, `yield_curve.py` |
| **geometry/** | `convex_hull.py`, `aabb.py`, `raycast.py`, `jarvis.py` |
| **graph/** | `dijkstra.py`, `bellman_ford.py`, `toposort.py`, `floyd_warshall.py`, `kruskal.py`, `prim.py`, `tarjan.py`, `edmonds_karp.py` |
| **knowledge/** | `graph.py`, `tfidf.py` |
| **logic/** | `sat_solver.py`, `resolution.py` |
| **matrix/** | `lu.py`, `qr.py`, `eigen.py`, `cholesky.py`, `determinant.py` |
| **ml/** | `numpy_net.py`, `bayes.py`, `kmeans.py`, `perceptron.py`, `logistic.py`, `linear_gd.py` |
| **net/** | `rate_limiter.py`, `circuit_breaker.py`, `retry.py`, `token_bucket.py`, `leaky_bucket.py` |
| **observability/** | `metrics.py`, `tracer.py`, `histogram.py` |
| **optim/** | `gradient.py`, `adam.py`, `sgd.py`, `rmsprop.py`, `adagrad.py`, `momentum.py` |
| **physics/** | `nbody.py`, `fractal.py`, `symbolic.py`, `integrator.py`, `collision.py`, `softbody.py`, `sph.py`, `gravity.py`, `barnes_hut.py`, `rigid_body.py`, `verlet_list.py` |
| **protocol/** | `http_parser.py`, `json_parser.py` |
| **quant/** | `black_scholes.py`, `monte_carlo.py`, `binomial_tree.py`, `portfolio.py`, `heston.py`, `vasicek.py`, `cir.py`, `garch.py`, `ornstein_uhlenbeck.py`, `bs_greeks.py` |
| **search/** | `astar.py`, `rrt.py`, `beam_search.py`, `ida_star.py` |
| **security/** | `password.py`, `hmac_auth.py` |
| **signal/** | `fft_filter.py`, `wavelet.py`, `convolution.py`, `goertzel.py`, `iir_filter.py` |
| **stats/** | `regression.py`, `bootstrap.py`, `distribution.py`, `hypothesis.py`, `kernel_density.py`, `pca.py`, `em_gmm.py` |
| **string/** | `kmp.py`, `edit_distance.py`, `rabin_karp.py`, `suffix_array.py`, `aho_corasick.py`, `z_algorithm.py`, `manacher.py` |

Root: `main.py`, `README.md`, `SECURITY.md`, `.gitignore`

---

## Run

Every module is independently executable:

```bash
python -m physics.nbody
python -m quant.black_scholes
python -m data.fenwick
python -m graph.tarjan
python -m crypto.pure_md5
python -m evolution.pso
# etc.
```

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
