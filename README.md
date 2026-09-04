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

## Package Inventory (latest)

All previously listed modules remain. Newly added in this round (40):

**data/**: `red_black.py`, `van_emde_boas.py`, `min_queue.py`, `fenwick2d.py`, `treap.py`, `splay_link.py`, `discontinuity.py`

**graph/**: `dinic.py`, `hungarian.py`, `min_cost_flow.py`, `kosaraju.py`, `hopcroft_karp.py`

**ml/**: `decision_stump.py`, `knn.py`, `random_forest.py`, `gradient_boosting.py`

**optim/**: `nesterov.py`, `adadelta.py`, `radam.py`, `lamb.py`

**finance/**: `nelson_siegel.py`

**quant/**: `hull_white.py`, `cir_pp.py`, `black_karasinski.py`

**signal/**: `savitzky_golay.py`, `median_filter.py`, `wiener.py`, `peak_detect.py`

**string/**: `suffix_automaton.py`

**crypto/**: `crc32.py`, `xxhash32.py`, `siphash.py`, `fnv1a.py`

**stats/**: `cusum.py`, `kalman_smoother.py`

**matrix/**: `sparse_csr.py`, `coo.py`

**physics/**: `hard_sphere.py`, `spring_damper.py`

**data (extra)**: `sliding_window_max.py`

Root: `main.py`, `README.md`, `SECURITY.md`, `.gitignore`

---

## Run

```bash
python -m data.red_black
python -m graph.dinic
python -m ml.knn
python -m quant.hull_white
python -m crypto.siphash
# etc.
```

```bash
python main.py
```

---

## Principles

1. Accuracy over completeness claims.
2. Only modules that exist in this repository are listed.
3. All implementations are original and self-contained.
4. Prefer verifiable numerical results over narrative claims.
5. Security-sensitive modules are for research; see SECURITY.md before reuse.
