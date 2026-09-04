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

**data/**: `avl.py`, `rope.py`, `scapegoat.py`, `btree_map.py`, `skip_list_map.py`, `fenwick_min.py`, `splay_map.py`, `segment_tree_lazy.py`

**graph/**: `min_cost_max_flow.py`, `blossom.py`, `push_relabel.py`, `cycle_canceling.py`, `capacity_scaling.py`

**ml/**: `isolation_forest.py`, `svm_smo.py`, `dbscan.py`, `optics.py`

**optim/**: `yogi.py`, `qhadam.py`, `ranger.py`, `adabelief.py`

**quant/**: `g2pp.py`, `hw1f.py`, `lmm.py`, `bdt.py`

**signal/**: `butterworth.py`, `wavelet_denoise.py`, `savgol_deriv.py`, `hilbert_huang.py`, `spectral_centroid.py`, `stft.py`, `mfcc_simple.py`

**crypto/**: `murmur3.py`, `cityhash.py`, `farmhash.py`, `spookyhash.py`

**stats/**: `kalman_2d.py`

**matrix/**: `csc.py`, `dok.py`, `lil.py`

All previous modules remain. Every new file is complete, original, and self-tested.

---

## Run

```bash
python -m data.avl
python -m graph.push_relabel
python -m ml.dbscan
python -m quant.g2pp
python -m crypto.murmur3
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
