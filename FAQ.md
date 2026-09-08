# Frequently Asked Questions

**Universe Simulator**

---

### What is this repository?

A private collection of independently executable, original Python modules covering algorithms, numerical methods, evolutionary computation, physics, quantitative finance, machine learning, signal processing, data structures, control theory, cryptography (research-only), graph algorithms, number theory, statistics, and core infrastructure. Every module is complete and carries its own self-test.

---

### Why are there so many modules?

The design goal is a broad, high-quality research kernel. Each module is deliberately self-contained so that any single algorithm can be studied, verified, or reused without pulling in a large framework.

---

### Do I need NumPy / SciPy / external libraries?

The majority of modules use only the Python standard library. A small number of numerical modules may import NumPy when it materially improves clarity or performance; any such dependency is declared in the module docstring. No module requires a network service or database.

---

### How do I run a module?

From the repository root:

```bash
python -m package.module_name
```

---

### What does “self-testing” mean?

Each module ends with an `if __name__ == "__main__"` block that executes real assertions (numerical tolerances, invariants, known reference values). A successful run prints a confirmation message and exits with code 0.

---

### Are the cryptographic modules safe for production secrets?

**No.** All modules under `crypto/` and `security/` are research and educational only. They are not formally audited. See SECURITY.md.

---

### Can I use these modules in a commercial product?

The repository is private and all rights are reserved by the owner. Redistribution or commercial use outside the authorised context requires explicit permission.

---

### Why do some self-tests take a few seconds?

Monte-Carlo, evolutionary, and N-body modules run enough iterations to produce statistically meaningful results. Defaults are chosen so that a typical laptop finishes them in a few seconds.

---

### How do I add a new module?

1. Place a complete, original implementation under the appropriate package.
2. Include a rigorous `if __name__ == "__main__"` self-test.
3. Run the test and a sample of sibling modules.
4. Commit only when the module is production-ready (no placeholders, no TODOs, no stubs).

---

### The self-test failed on my machine but passed on another. What now?

Floating-point differences across platforms occasionally surface. Check the printed actual value against the tolerance. If the algorithm is still correct, a modest widening of the tolerance is acceptable after verification. See TROUBLESHOOTING.md.

---

### Is there a single test runner?

Any module can be executed directly. For broader coverage, a simple loop over a package or the `main.py` entry point serves as a smoke test. See OPERATIONS.md and TEST_SUITES.md.

---

### Where is the documentation for a specific algorithm?

Each module begins with a docstring that states purpose, complexity, and any important assumptions. MODULE_CATALOG.md gives a one-sentence summary of every module.

---

### How is numerical correctness verified?

Against known analytic results, invariants (energy conservation, orthogonality, reconstruction error, statistical moments), and cross-checks with independent implementations where feasible.

---

### Who maintains this repository?

The owner of the `observabilityengine` organisation. Security-relevant issues should be reported privately (see SECURITY.md).

---

*If your question is not answered here, consult OPERATIONS.md, TROUBLESHOOTING.md, TEST_SUITES.md, SECURITY.md, and the module source itself.*
