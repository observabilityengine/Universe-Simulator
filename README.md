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

## Latest additions (40 modules)

**data/**: `cartesian_map`, `wavelet_tree`, `van_emde_map`, `order_stat_tree`, `fm_sketch`, `radix_tree`, `hyperloglog`

**graph/**: `dinic_scaling`, `mcmf_cost_scaling`, `densest_subgraph`, `edmonds_matching`, `karger_mincut`, `stoer_wagner`

**ml/**: `xgboost_reg`, `spectral_clustering`, `mean_shift`, `gmm_em`

**optim/**: `lion`, `sophia`, `adan`

**quant/**: `cir_exact`, `hw2f`, `bachelier`, `sabr`

**signal/**: `iir_notch`, `chebyshev`, `goertzel_bank`, `biquad`, `chroma`, `allpass`, `tonnetz`

**crypto/**: `blake2s`, `poly1305`, `argon2_stub`, `scrypt_stub`

**mathlib/**: `lambert_w`

**string/**: `suffix_tree`

**matrix/**: `ellpack`, `dia`, `bsr`

All previous modules remain. Every new file is complete, original, and self-tested.

---

## Run

```bash
python -m data.hyperloglog
python -m graph.stoer_wagner
python -m ml.gmm_em
python -m quant.sabr
python -m crypto.blake2s
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
